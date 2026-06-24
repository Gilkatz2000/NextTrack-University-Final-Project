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

    selected_reasons = reasons[:3]

    return "Recommended because it " + ", ".join(selected_reasons) + "."