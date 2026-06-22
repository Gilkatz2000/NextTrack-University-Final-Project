from app.data_loader import load_tracks


def build_v2_reason(row, genres, mood, seed_artists):
    reasons = []

    if row["genre"] in genres:
        reasons.append("matched the requested genre")

    if row["mood"] == mood:
        reasons.append("matched the requested mood")

    if row["artist"] in seed_artists:
        reasons.append("matched one of the seed artists")

    if not reasons:
        reasons.append("had a strong overall weighted score")

    return "This track was recommended because it " + ", ".join(reasons) + "."


def get_recommendations_v2(genres, mood, seed_artists, limit=5):
    df = load_tracks()

    genres = [genre.lower() for genre in genres]
    mood = mood.lower()
    seed_artists = [artist.lower() for artist in seed_artists]

    df["genre"] = df["genre"].str.lower()
    df["mood"] = df["mood"].str.lower()
    df["artist"] = df["artist"].str.lower()

    max_popularity = df["popularity"].max()

    df["genre_score"] = df["genre"].apply(lambda genre: 1 if genre in genres else 0)
    df["mood_score"] = df["mood"].apply(lambda track_mood: 1 if track_mood == mood else 0)
    df["artist_score"] = df["artist"].apply(lambda artist: 1 if artist in seed_artists else 0)
    df["popularity_score"] = df["popularity"] / max_popularity
    df["energy_score"] = df["energy"]
    df["danceability_score"] = df["danceability"]
    df["valence_score"] = df["valence"]

    df["score"] = (
        0.30 * df["genre_score"]
        + 0.25 * df["mood_score"]
        + 0.15 * df["artist_score"]
        + 0.10 * df["popularity_score"]
        + 0.10 * df["energy_score"]
        + 0.05 * df["danceability_score"]
        + 0.05 * df["valence_score"]
    )

    ranked_tracks = df.sort_values(by="score", ascending=False)

    return apply_diversity_filter_v2(ranked_tracks, genres, mood, seed_artists, limit)


def apply_diversity_filter_v2(ranked_tracks, genres, mood, seed_artists, limit):
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
            "spotify_url": row["spotify_url"],
            "score": round(float(row["score"]), 3),
            "reason": build_v2_reason(row, genres, mood, seed_artists),
        }

        recommendations.append(recommendation)

        artist_count[artist] = artist_count.get(artist, 0) + 1
        genre_count[genre] = genre_count.get(genre, 0) + 1

        if len(recommendations) == limit:
            break

    return recommendations