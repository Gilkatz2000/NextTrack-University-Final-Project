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

    genres = [g.lower() for g in genres]
    seed_artists = [a.lower() for a in seed_artists]
    mood = mood.lower()

    df["genre"] = df["genre"].str.lower()
    df["mood"] = df["mood"].str.lower()
    df["artist"] = df["artist"].str.lower()

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

    diversified = apply_diversity_filter(
        ranked_tracks,
        genres,
        mood,
        seed_artists,
        limit,
    )

    return diversified


def apply_diversity_filter(ranked_tracks, genres, mood, seed_artists, limit):
    recommendations = []
    artist_count = {}
    genre_count = {}

    for _, row in ranked_tracks.iterrows():
        artist = row["artist"]
        genre = row["genre"]

        if artist_count.get(artist, 0) >= 2:
            continue

        if genre_count.get(genre, 0) >= 3:
            continue

        recommendation = {
            "track": row["track"],
            "artist": row["artist"].title(),
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
                genres,
                mood,
                seed_artists,
            ),
            "spotify_url": build_spotify_search_url(
                row["track"],
                row["artist"],
            ),
            "youtube_url": build_youtube_search_url(
                row["track"],
                row["artist"],
            ),
        }

        if "spotify_track_id" in row.index and pd.notna(row["spotify_track_id"]):
            spotify_track_id = str(row["spotify_track_id"]).strip()
            if spotify_track_id:
                recommendation["spotify_track_id"] = spotify_track_id

        recommendations.append(recommendation)

        artist_count[artist] = artist_count.get(artist, 0) + 1
        genre_count[genre] = genre_count.get(genre, 0) + 1

        if len(recommendations) == limit:
            break

    return recommendations