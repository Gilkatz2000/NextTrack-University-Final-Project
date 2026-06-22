import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from urllib.parse import quote_plus

from app.data_loader import load_tracks

def build_recommendation_reason(track, genres, mood, seed_artists):
    reasons = []

    track_genre = track["genre"]
    track_mood = track["mood"]
    track_artist = track["artist"]

    if track_genre in genres and track_mood == mood:
        reasons.append("matches both your selected genre and mood")
    elif track_genre in genres:
        reasons.append("matches your selected genre")
    elif track_mood == mood:
        reasons.append("matches your selected mood")

    if track_artist in seed_artists:
        reasons.append("uses an artist you already like")

    if float(track["energy"]) >= 0.75:
        reasons.append("has a high energy level")
    elif float(track["energy"]) <= 0.35:
        reasons.append("has a calmer sound")

    if float(track["danceability"]) >= 0.70:
        reasons.append("has strong danceability")

    if int(track["popularity"]) >= 75:
        reasons.append("is a popular track in the dataset")

    if int(track["release_year"]) >= 2018:
        reasons.append("is a relatively recent release")

    if not reasons:
        reasons.append("has the closest overall similarity to your current session choices")

    # Keep the explanation short and readable in the frontend.
    selected_reasons = reasons[:3]

    return "Recommended because it " + ", ".join(selected_reasons) + "."

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
        columns=["genre", "mood", "artist"]
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
    session_vector["danceability"] = 0.70
    session_vector["valence"] = 0.65
    session_vector["release_year"] = 0.85

    similarity_scores = cosine_similarity(session_vector, encoded_features)[0]

    df["score"] = similarity_scores

    ranked_tracks = df.sort_values(by="score", ascending=False)

    diversified = apply_diversity_filter(
        ranked_tracks,
        genres,
        mood,
        seed_artists,
        limit
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
            "score": round(float(row["score"]), 3),
            "reason": build_recommendation_reason(
                row,
                genres,
                mood,
                seed_artists
            ),
        }

        spotify_query = quote_plus(f"{row['track']} {row['artist']}")
        recommendation["spotify_url"] = f"https://open.spotify.com/search/{spotify_query}"

        recommendations.append(recommendation)

        artist_count[artist] = artist_count.get(artist, 0) + 1
        genre_count[genre] = genre_count.get(genre, 0) + 1

        if len(recommendations) == limit:
            break

    return recommendations