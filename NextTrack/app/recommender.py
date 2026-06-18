import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

DATASET_PATH = Path(__file__).parent / "dataset.csv"


def build_recommendation_reason(track, genres, mood, seed_artists):
    reasons = []

    if track["genre"] in genres:
        reasons.append("matched the requested genre")

    if track["mood"] == mood:
        reasons.append("matched the requested mood")

    if track["artist"] in seed_artists:
        reasons.append("matched one of the seed artists")

    if not reasons:
        reasons.append("was selected based on overall similarity")

    return "This track was recommended because it " + ", ".join(reasons) + "."


def get_recommendations(genres, mood, seed_artists, limit=5):
    df = pd.read_csv(DATASET_PATH)

    genres = [g.lower() for g in genres]
    seed_artists = [a.lower() for a in seed_artists]
    mood = mood.lower()

    df["genre"] = df["genre"].str.lower()
    df["mood"] = df["mood"].str.lower()
    df["artist"] = df["artist"].str.lower()

    feature_df = df[["genre", "mood", "artist", "tempo", "energy", "popularity"]].copy()

    encoded_features = pd.get_dummies(
        feature_df,
        columns=["genre", "mood", "artist"]
    )

    scaler = MinMaxScaler()
    encoded_features[["tempo", "energy", "popularity"]] = scaler.fit_transform(
        encoded_features[["tempo", "energy", "popularity"]]
    )

    session_vector = pd.DataFrame(
        0,
        index=[0],
        columns=encoded_features.columns
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

    similarity_scores = cosine_similarity(session_vector, encoded_features)[0]

    df["score"] = similarity_scores

    ranked_tracks = df.sort_values(by="score", ascending=False)

    diversified = apply_diversity_filter(ranked_tracks, genres, mood, seed_artists, limit)

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

        recommendations.append({
            "track": row["track"],
            "artist": row["artist"].title(),
            "genre": row["genre"],
            "mood": row["mood"],
            "tempo": int(row["tempo"]),
            "energy": float(row["energy"]),
            "popularity": int(row["popularity"]),
            "score": round(float(row["score"]), 3),
            "reason": build_recommendation_reason(row, genres, mood, seed_artists),
        })

        artist_count[artist] = artist_count.get(artist, 0) + 1
        genre_count[genre] = genre_count.get(genre, 0) + 1

        if len(recommendations) == limit:
            break

    return recommendations