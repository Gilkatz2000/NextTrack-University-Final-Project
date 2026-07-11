"""Content-based recommendation engine for NextTrack.

The engine remains stateless: every request is converted into a temporary session
profile and discarded after recommendations are returned. Ranking combines cosine
similarity, explicit preference matching, mood-aware audio similarity and similarity
to the selected artist's catalogue. A soft diversity reranker then encourages variety
without forcing weak genre matches into the result set.
"""

from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from app.data_loader import load_tracks
from app.services.recommendation_links import (
    build_spotify_search_url,
    build_youtube_search_url,
)
from app.services.recommendation_reasons import build_recommendation_reason


# These profiles represent the expected audio characteristics of each mood.
# They are temporary content-based targets and are not stored between sessions.
MOOD_PROFILES = {
    "happy": {
        "tempo": 0.62,
        "energy": 0.72,
        "danceability": 0.74,
        "valence": 0.88,
    },
    "sad": {
        "tempo": 0.30,
        "energy": 0.30,
        "danceability": 0.36,
        "valence": 0.18,
    },
    "calm": {
        "tempo": 0.25,
        "energy": 0.22,
        "danceability": 0.38,
        "valence": 0.52,
    },
    "angry": {
        "tempo": 0.63,
        "energy": 0.92,
        "danceability": 0.43,
        "valence": 0.25,
    },
    "dark": {
        "tempo": 0.45,
        "energy": 0.58,
        "danceability": 0.43,
        "valence": 0.20,
    },
    "party": {
        "tempo": 0.66,
        "energy": 0.88,
        "danceability": 0.90,
        "valence": 0.78,
    },
    "energetic": {
        "tempo": 0.72,
        "energy": 0.92,
        "danceability": 0.70,
        "valence": 0.64,
    },
    "romantic": {
        "tempo": 0.38,
        "energy": 0.45,
        "danceability": 0.57,
        "valence": 0.62,
    },
    "inspirational": {
        "tempo": 0.50,
        "energy": 0.68,
        "danceability": 0.52,
        "valence": 0.78,
    },
    "chill": {
        "tempo": 0.36,
        "energy": 0.36,
        "danceability": 0.58,
        "valence": 0.57,
    },
    "cool": {
        "tempo": 0.46,
        "energy": 0.56,
        "danceability": 0.70,
        "valence": 0.55,
    },
    "nostalgic": {
        "tempo": 0.40,
        "energy": 0.44,
        "danceability": 0.48,
        "valence": 0.50,
    },
}


DEFAULT_MOOD_PROFILE = {
    "tempo": 0.50,
    "energy": 0.55,
    "danceability": 0.55,
    "valence": 0.50,
}


AUDIO_COLUMNS = [
    "tempo",
    "energy",
    "danceability",
    "valence",
]


NUMERIC_COLUMNS = [
    "tempo",
    "energy",
    "popularity",
    "danceability",
    "valence",
    "release_year",
]


def _normalise_inputs(values):
    """Return cleaned lowercase values while ignoring empty input."""

    return [
        str(value).strip().lower()
        for value in values
        if str(value).strip()
    ]


def _build_artist_profile(
    df,
    scaled_numeric,
    seed_artists,
):
    """Build a temporary profile from the selected artists' tracks.

    The profile contains:

    - average audio characteristics
    - genres associated with the artist
    - moods associated with the artist

    The profile exists only during the current recommendation request.
    """

    if not seed_artists:
        return None

    artist_mask = df["artist"].isin(seed_artists)

    if not artist_mask.any():
        return None

    artist_rows = df.loc[artist_mask]

    return {
        "audio": scaled_numeric.loc[
            artist_mask,
            AUDIO_COLUMNS,
        ].mean(),
        "genres": set(artist_rows["genre"]),
        "moods": set(artist_rows["mood"]),
    }


def _audio_similarity(
    scaled_numeric,
    target_profile,
):
    """Calculate similarity to a target audio profile.

    Similarity is based on the mean absolute distance between the track's
    audio values and the temporary mood profile.

    The returned value remains between 0 and 1.
    """

    target_values = np.array(
        [
            target_profile[column]
            for column in AUDIO_COLUMNS
        ]
    )

    track_values = scaled_numeric[
        AUDIO_COLUMNS
    ].to_numpy(dtype=float)

    mean_absolute_distance = np.abs(
        track_values - target_values
    ).mean(axis=1)

    return np.clip(
        1.0 - mean_absolute_distance,
        0.0,
        1.0,
    )


def _artist_similarity(
    df,
    scaled_numeric,
    artist_profile,
    seed_artists,
):
    """Calculate content-based similarity to the selected artist profile."""

    if artist_profile is None:
        return np.zeros(
            len(df),
            dtype=float,
        )

    target_values = artist_profile[
        "audio"
    ].to_numpy(dtype=float)

    track_values = scaled_numeric[
        AUDIO_COLUMNS
    ].to_numpy(dtype=float)

    audio_similarity = np.clip(
        1.0
        - np.abs(
            track_values - target_values
        ).mean(axis=1),
        0.0,
        1.0,
    )

    genre_affinity = (
        df["genre"]
        .isin(artist_profile["genres"])
        .astype(float)
        .to_numpy()
    )

    mood_affinity = (
        df["mood"]
        .isin(artist_profile["moods"])
        .astype(float)
        .to_numpy()
    )

    exact_artist_match = (
        df["artist"]
        .isin(seed_artists)
        .astype(float)
        .to_numpy()
    )

    return np.clip(
        0.60 * audio_similarity
        + 0.18 * genre_affinity
        + 0.12 * mood_affinity
        + 0.10 * exact_artist_match,
        0.0,
        1.0,
    )


def _artist_profile_compatibility(
    artist_profile,
    mood_profile,
    selected_genres,
    selected_mood,
):
    """Measure whether the selected artist fits the current session.

    Artist influence becomes stronger when the artist's catalogue is compatible
    with the selected genre and mood. Conflicting artists still influence ranking,
    but they do not overpower the user's explicit current-session choices.
    """

    if artist_profile is None:
        return 0.0

    artist_audio = artist_profile["audio"]

    audio_distance = np.mean(
        [
            abs(
                float(artist_audio[column])
                - float(mood_profile[column])
            )
            for column in AUDIO_COLUMNS
        ]
    )

    audio_compatibility = max(
        0.0,
        min(
            1.0,
            1.0 - audio_distance,
        ),
    )

    genre_overlap = (
        1.0
        if artist_profile["genres"].intersection(
            selected_genres
        )
        else 0.0
    )

    mood_overlap = (
        1.0
        if selected_mood
        in artist_profile["moods"]
        else 0.0
    )

    return float(
        np.clip(
            0.65 * audio_compatibility
            + 0.25 * genre_overlap
            + 0.10 * mood_overlap,
            0.0,
            1.0,
        )
    )


def get_recommendations(
    genres,
    mood,
    seed_artists,
    limit=10,
):
    """Generate stateless recommendations from the current session input."""

    df = load_tracks().copy()

    genres = list(
        dict.fromkeys(
            _normalise_inputs(genres)
        )
    )

    seed_artists = list(
        dict.fromkeys(
            _normalise_inputs(seed_artists)
        )
    )

    mood = str(mood).strip().lower()
    limit = max(1, int(limit))

    # Preserve the original formatting for frontend display.
    df["display_track"] = (
        df["track"]
        .astype(str)
        .str.strip()
    )

    df["display_artist"] = (
        df["artist"]
        .astype(str)
        .str.strip()
    )

    # Normalised values are used internally for matching.
    df["genre"] = (
        df["genre"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["mood"] = (
        df["mood"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["artist"] = (
        df["artist"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    scaler = MinMaxScaler()

    scaled_numeric = pd.DataFrame(
        scaler.fit_transform(
            df[NUMERIC_COLUMNS]
        ),
        columns=NUMERIC_COLUMNS,
        index=df.index,
    )

    feature_df = pd.concat(
        [
            scaled_numeric,
            pd.get_dummies(
                df[
                    [
                        "genre",
                        "mood",
                        "artist",
                    ]
                ],
                dtype=float,
            ),
        ],
        axis=1,
    )

    session_vector = pd.DataFrame(
        0.0,
        index=[0],
        columns=feature_df.columns,
    )

    # Add selected genres to the temporary session vector.
    for genre in genres:
        genre_column = f"genre_{genre}"

        if genre_column in session_vector.columns:
            session_vector.at[
                0,
                genre_column,
            ] = 1.0

    # Add the selected mood label.
    mood_column = f"mood_{mood}"

    if mood_column in session_vector.columns:
        session_vector.at[
            0,
            mood_column,
        ] = 1.0

    # Add exact artist indicators when those artists exist in the dataset.
    for artist in seed_artists:
        artist_column = f"artist_{artist}"

        if artist_column in session_vector.columns:
            session_vector.at[
                0,
                artist_column,
            ] = 1.0

    # The numerical session profile now changes according to the selected mood.
    mood_profile = MOOD_PROFILES.get(
        mood,
        DEFAULT_MOOD_PROFILE,
    )

    for column, target_value in mood_profile.items():
        session_vector.at[
            0,
            column,
        ] = target_value

    # Popularity and recency remain neutral in the session vector.
    # They are used only as small tie-breaking signals later.
    session_vector.at[
        0,
        "popularity",
    ] = 0.50

    session_vector.at[
        0,
        "release_year",
    ] = 0.50

    # Build a temporary content-based profile for the selected artist.
    artist_profile = _build_artist_profile(
        df,
        scaled_numeric,
        seed_artists,
    )

    artist_compatibility = _artist_profile_compatibility(
        artist_profile,
        mood_profile,
        set(genres),
        mood,
    )

    if artist_profile is not None:
        artist_blend = (
            0.12
            + 0.18 * artist_compatibility
        )

        mood_blend = (
            1.0
            - artist_blend
        )

        for column in AUDIO_COLUMNS:
            session_vector.at[
                0,
                column,
            ] = (
                mood_blend
                * mood_profile[column]
                + artist_blend
                * float(
                    artist_profile["audio"][column]
                )
            )

    # Cosine similarity remains a central part of the recommender.
    df["cosine_score"] = cosine_similarity(
        session_vector,
        feature_df,
    )[0]

    df["genre_score"] = (
        df["genre"]
        .isin(genres)
        .astype(float)
    )

    df["mood_label_score"] = (
        df["mood"] == mood
    ).astype(float)

    df["mood_audio_score"] = _audio_similarity(
        scaled_numeric,
        mood_profile,
    )

    df["artist_similarity_score"] = _artist_similarity(
        df,
        scaled_numeric,
        artist_profile,
        seed_artists,
    )

    df["popularity_score"] = scaled_numeric[
        "popularity"
    ]

    df["recency_score"] = scaled_numeric[
        "release_year"
    ]

    # Artist influence depends on how compatible the selected artist is
    # with the current genre and mood preferences.
    if artist_profile is None:
        artist_weight = 0.0

    else:
        artist_weight = (
            0.05
            + 0.10 * artist_compatibility
        )

    base_score = (
        0.20
        * df["cosine_score"]
        + 0.30
        * df["genre_score"]
        + 0.20
        * df["mood_label_score"]
        + 0.15
        * df["mood_audio_score"]
        + artist_weight
        * df["artist_similarity_score"]
        + 0.03
        * df["popularity_score"]
        + 0.02
        * df["recency_score"]
    )

    total_weight = (
        0.20
        + 0.30
        + 0.20
        + 0.15
        + artist_weight
        + 0.03
        + 0.02
    )

    df["adjusted_score"] = (
        base_score
        / total_weight
    ).clip(
        0.0,
        1.0,
    )

    # Keep single-genre sessions focused on the selected genre.
    # Multiple-genre sessions still allow broader discovery.
    if genres:
        outside_genre_penalty = (
            0.18
            if len(genres) == 1
            else 0.10
        )

        df["adjusted_score"] -= (
            ~df["genre"].isin(genres)
        ).astype(float) * outside_genre_penalty

    df["adjusted_score"] = (
        df["adjusted_score"]
        .clip(
            0.0,
            1.0,
        )
    )

    ranked_tracks = df.sort_values(
        by=[
            "adjusted_score",
            "mood_label_score",
            "genre_score",
        ],
        ascending=[
            False,
            False,
            False,
        ],
    )

    # Use a sufficiently large candidate pool for diversity reranking.
    candidate_pool = ranked_tracks.head(
        max(
            120,
            limit * 15,
        )
    ).copy()

    # Ensure selected genres remain available to the diversity reranker.
    candidate_frames = [
        candidate_pool
    ]

    if genres:
        candidate_frames.append(
            ranked_tracks[
                ranked_tracks["genre"].isin(genres)
            ].head(
                max(
                    80,
                    limit * 10,
                )
            )
        )

    # Ensure exact mood matches remain available.
    candidate_frames.append(
        ranked_tracks[
            ranked_tracks["mood"] == mood
        ].head(
            max(
                60,
                limit * 8,
            )
        )
    )

    candidate_pool = (
        pd.concat(candidate_frames)
        .drop_duplicates(
            subset=[
                "display_track",
                "display_artist",
            ]
        )
        .sort_values(
            by="adjusted_score",
            ascending=False,
        )
    )

    return apply_diversity_filter(
        candidate_pool,
        genres,
        mood,
        seed_artists,
        limit,
        mood_profile,
    )


def apply_diversity_filter(
    ranked_tracks,
    genres,
    mood,
    seed_artists,
    limit,
    mood_profile=None,
):
    """Select relevant recommendations using soft diversity penalties.

    Relevance remains the dominant factor.

    Diversity encourages variety but does not reserve positions for weak
    recommendations merely because they belong to an uncovered genre.
    """

    selected_indices = []
    selected_keys = set()
    used_artists = set()

    genre_counts = Counter()
    selected_genres_covered = set()

    selected_genres = list(
        dict.fromkeys(genres)
    )

    candidates = ranked_tracks.copy()

    def recommendation_key(row):
        return (
            str(
                row["display_track"]
            ).strip().lower(),
            str(
                row["display_artist"]
            ).strip().lower(),
        )

    while len(selected_indices) < limit:
        best_index = None
        best_utility = -float("inf")

        for index, row in candidates.iterrows():
            key = recommendation_key(row)

            artist = str(
                row["artist"]
            ).strip().lower()

            genre = str(
                row["genre"]
            ).strip().lower()

            # Avoid duplicate tracks and repeated artists.
            if (
                key in selected_keys
                or artist in used_artists
            ):
                continue

            relevance = float(
                row["adjusted_score"]
            )
            
            utility = relevance
            
            if len(selected_genres) > 1:
                utility -= (
                    0.045
                    * genre_counts[genre]
                )

            else:
                utility -= (
                    0.010
                    * genre_counts[genre]
                )

            # Small bonus for covering another selected genre,
            # but only when the candidate is reasonably relevant.
            if (
                genre in selected_genres
                and genre
                not in selected_genres_covered
                and relevance >= 0.58
            ):
                utility += 0.035

            # Prefer exact mood matches when candidates are otherwise close.
            if (
                str(
                    row["mood"]
                ).strip().lower()
                == mood
            ):
                utility += 0.018

            # Avoid three consecutive recommendations from the same genre.
            if len(selected_indices) >= 2:
                previous_genres = [
                    str(
                        candidates.loc[
                            selected_index,
                            "genre",
                        ]
                    )
                    .strip()
                    .lower()
                    for selected_index
                    in selected_indices[-2:]
                ]

                if (
                    previous_genres[0]
                    == previous_genres[1]
                    == genre
                ):
                    utility -= 0.08

            if utility > best_utility:
                best_utility = utility
                best_index = index

        if best_index is None:
            break

        selected_row = candidates.loc[
            best_index
        ]

        selected_indices.append(
            best_index
        )

        selected_keys.add(
            recommendation_key(
                selected_row
            )
        )

        selected_artist = str(
            selected_row["artist"]
        ).strip().lower()

        selected_genre = str(
            selected_row["genre"]
        ).strip().lower()

        used_artists.add(
            selected_artist
        )

        genre_counts[
            selected_genre
        ] += 1

        if selected_genre in selected_genres:
            selected_genres_covered.add(
                selected_genre
            )

    selected = candidates.loc[
        selected_indices
    ].copy()

    # The diversity algorithm decides membership.
    # Final presentation is still ordered by match score.
    selected = selected.sort_values(
        by="adjusted_score",
        ascending=False,
    )

    recommendations = []

    for _, row in selected.iterrows():
        recommendation = {
            "track": row["display_track"],
            "artist": row["display_artist"],
            "genre": row["genre"],
            "mood": row["mood"],
            "tempo": int(row["tempo"]),
            "energy": float(row["energy"]),
            "popularity": int(
                row["popularity"]
            ),
            "danceability": float(
                row["danceability"]
            ),
            "valence": float(
                row["valence"]
            ),
            "release_year": int(
                row["release_year"]
            ),
            "score": round(
                float(
                    row["adjusted_score"]
                ),
                3,
            ),
            "reason": build_recommendation_reason(
                row,
                selected_genres,
                mood,
                seed_artists,
                mood_profile=(
                    mood_profile
                    or MOOD_PROFILES.get(
                        mood,
                        DEFAULT_MOOD_PROFILE,
                    )
                ),
            ),
            "spotify_url": build_spotify_search_url(
                row["display_track"],
                row["display_artist"],
            ),
            "youtube_url": build_youtube_search_url(
                row["display_track"],
                row["display_artist"],
            ),
        }

        if (
            "spotify_track_id" in row.index
            and pd.notna(
                row["spotify_track_id"]
            )
        ):
            spotify_track_id = str(
                row["spotify_track_id"]
            ).strip()

            if spotify_track_id:
                recommendation[
                    "spotify_track_id"
                ] = spotify_track_id

        recommendations.append(
            recommendation
        )

    return recommendations