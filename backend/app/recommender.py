import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from app.data_loader import load_tracks
from app.services.recommendation_links import (
    build_spotify_search_url,
    build_youtube_search_url,
)
from app.services.recommendation_reasons import build_recommendation_reason


def get_recommendations(genres, mood, seed_artists, limit=10):
    df = load_tracks()

    genres = [str(g).strip().lower() for g in genres]
    seed_artists = [
        str(artist).strip().lower()
        for artist in seed_artists
    ]
    mood = str(mood).strip().lower()

    df["display_track"] = df["track"].astype(str).str.strip()
    df["display_artist"] = df["artist"].astype(str).str.strip()

    df["genre"] = df["genre"].astype(str).str.strip().str.lower()
    df["mood"] = df["mood"].astype(str).str.strip().str.lower()
    df["artist"] = df["artist"].astype(str).str.strip().str.lower()

    feature_df = df[
        [
            "genre",
            "mood",
            "artist",
            "tempo",
            "energy",
            "popularity",
            "danceability",
            "valence",
            "release_year",
        ]
    ].copy()

    encoded_features = pd.get_dummies(
        feature_df,
        columns=["genre", "mood", "artist"],
    )

    numeric_columns = [
        "tempo",
        "energy",
        "popularity",
        "danceability",
        "valence",
        "release_year",
    ]

    scaler = MinMaxScaler()
    encoded_features[numeric_columns] = scaler.fit_transform(
        encoded_features[numeric_columns]
    )

    session_vector = pd.DataFrame(
        0,
        index=[0],
        columns=encoded_features.columns,
    )

    for genre in genres:
        column = f"genre_{genre}"
        if column in session_vector.columns:
            session_vector[column] = 1

    mood_column = f"mood_{mood}"
    if mood_column in session_vector.columns:
        session_vector[mood_column] = 1

    for artist in seed_artists:
        column = f"artist_{artist}"
        if column in session_vector.columns:
            session_vector[column] = 1

    session_vector["energy"] = 0.85
    session_vector["tempo"] = 0.80
    session_vector["popularity"] = 0.50
    session_vector["danceability"] = 0.70
    session_vector["valence"] = 0.65
    session_vector["release_year"] = 0.85

    similarity_scores = cosine_similarity(session_vector, encoded_features)[0]

    df["score"] = similarity_scores
    df["adjusted_score"] = df["score"]

    # Ranking priority:
    # 1. Tracks matching both selected genre and mood
    # 2. Tracks matching selected genre
    # 3. Tracks matching selected mood
    # 4. General cosine similarity fallback
    df.loc[
        (df["genre"].isin(genres)) & (df["mood"] == mood),
        "adjusted_score",
    ] += 0.40

    df.loc[
        df["genre"].isin(genres),
        "adjusted_score",
    ] += 0.25

    df.loc[
        df["mood"] == mood,
        "adjusted_score",
    ] += 0.15

    df.loc[
        df["artist"].isin(seed_artists),
        "adjusted_score",
    ] += 0.10

    df["adjusted_score"] = df["adjusted_score"].clip(upper=1.0)

    ranked_tracks = df.sort_values(
        by="adjusted_score",
        ascending=False,
    )

    candidate_frames = [ranked_tracks.head(max(50, limit * 5))]

    for genre in genres:
        genre_candidates = ranked_tracks[
            ranked_tracks["genre"] == genre
        ].head(max(15, limit * 2))

        candidate_frames.append(genre_candidates)

    candidate_pool = (
        pd.concat(candidate_frames)
        .drop_duplicates(subset=["track", "artist"])
        .sort_values(by="adjusted_score", ascending=False)
    )

    diversified = apply_diversity_filter(
        candidate_pool,
        genres,
        mood,
        seed_artists,
        limit,
    )

    return diversified


def apply_diversity_filter(
    ranked_tracks,
    genres,
    mood,
    seed_artists,
    limit,
):
    recommendations = []
    selected_keys = set()
    used_artists = set()
    genre_count = {}

    selected_genres = list(dict.fromkeys(genres))

    has_preference_matches = (
        ranked_tracks["genre"].isin(selected_genres)
        | (ranked_tracks["mood"] == mood)
    ).any()

    def track_key(row):
        """Return a normalized identifier for duplicate prevention."""
        return (
            str(row["track"]).strip().lower(),
            str(row["artist"]).strip().lower(),
        )

    def can_select(row, enforce_run_rule=True):
        """Check whether a candidate satisfies the diversity rules."""
        artist = str(row["artist"]).strip().lower()
        key = track_key(row)
        genre = row["genre"]

        if key in selected_keys:
            return False

        # Maximum one recommendation per artist.
        if artist in used_artists:
            return False

        genre_matches = genre in selected_genres
        mood_matches = row["mood"] == mood

        # When valid preferences exist, avoid unrelated fallback tracks until
        # the final fill stage.
        if (
            has_preference_matches
            and not genre_matches
            and not mood_matches
        ):
            return False

        # Never show three consecutive tracks from the same genre.
        if enforce_run_rule and len(recommendations) >= 2:
            previous_genre = recommendations[-1]["genre"]
            second_previous_genre = recommendations[-2]["genre"]

            if (
                genre == previous_genre
                and genre == second_previous_genre
            ):
                return False

        return True

    def add_recommendation(row):
        """Convert a dataframe row and add it to the final results."""
        artist = str(row["artist"]).strip().lower()
        genre = row["genre"]
        key = track_key(row)

        recommendation = {
            "track": row["display_track"],
            "artist": row["display_artist"],
            "genre": row["genre"],
            "mood": row["mood"],
            "tempo": int(row["tempo"]),
            "energy": float(row["energy"]),
            "popularity": int(row["popularity"]),
            "danceability": float(row["danceability"]),
            "valence": float(row["valence"]),
            "release_year": int(row["release_year"]),
            "score": round(float(row["adjusted_score"]), 3),
            "reason": build_recommendation_reason(
                row,
                selected_genres,
                mood,
                seed_artists,
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
            and pd.notna(row["spotify_track_id"])
        ):
            spotify_track_id = str(
                row["spotify_track_id"]
            ).strip()

            if spotify_track_id:
                recommendation["spotify_track_id"] = spotify_track_id

        recommendations.append(recommendation)
        selected_keys.add(key)
        used_artists.add(artist)
        genre_count[genre] = genre_count.get(genre, 0) + 1

    if selected_genres:
        # Divide the available positions as evenly as possible.
        #
        # Example:
        # 10 results and 3 selected genres -> quotas of 4, 3 and 3.
        base_quota = limit // len(selected_genres)
        remainder = limit % len(selected_genres)

        genre_quotas = {
            genre: base_quota + (1 if index < remainder else 0)
            for index, genre in enumerate(selected_genres)
        }

        genre_candidates = {}

        for genre in selected_genres:
            candidates = ranked_tracks[
                ranked_tracks["genre"] == genre
            ].copy()

            # Within each genre, exact mood matches come first. The original
            # adjusted score remains the secondary ordering criterion.
            candidates["exact_mood_match"] = (
                candidates["mood"] == mood
            ).astype(int)

            candidates = candidates.sort_values(
                by=["exact_mood_match", "adjusted_score"],
                ascending=[False, False],
            )

            genre_candidates[genre] = candidates

        # Round-robin selection prevents the first selected genre from taking
        # all of the highest positions.
        progress_made = True

        while len(recommendations) < limit and progress_made:
            progress_made = False

            for genre in selected_genres:
                if len(recommendations) >= limit:
                    break

                if genre_count.get(genre, 0) >= genre_quotas[genre]:
                    continue

                candidates = genre_candidates[genre]

                for _, row in candidates.iterrows():
                    if not can_select(row):
                        continue

                    add_recommendation(row)
                    progress_made = True
                    break

    # Fill unused positions from the strongest remaining candidates.
    #
    # This is necessary when one selected genre has too few suitable tracks or
    # its candidates are rejected due to the one-track-per-artist rule.
    for _, row in ranked_tracks.iterrows():
        if len(recommendations) >= limit:
            break

        if can_select(row):
            add_recommendation(row)

    # Final safety fallback: relax only the consecutive-genre rule. Artist and
    # duplicate protections remain active.
    for _, row in ranked_tracks.iterrows():
        if len(recommendations) >= limit:
            break

        if can_select(row, enforce_run_rule=False):
            add_recommendation(row)

    return recommendations