def build_recommendation_reason(track, genres, mood, seed_artists):
    reasons = []

    track_genre = str(track["genre"]).lower()
    track_mood = str(track["mood"]).lower()
    track_artist = str(track["artist"]).lower()

    selected_genres = [str(genre).lower() for genre in genres]
    selected_mood = str(mood).lower()
    selected_artists = [str(artist).lower() for artist in seed_artists]

    if track_genre in selected_genres and track_mood == selected_mood:
        reasons.append("matches both your selected genre and mood")
    elif track_genre in selected_genres:
        reasons.append("matches your selected genre")
    elif track_mood == selected_mood:
        reasons.append("matches your selected mood and adds variety to your recommendations")

    if track_artist in selected_artists:
        reasons.append("uses an artist you already like")

    if float(track["energy"]) >= 0.75:
        reasons.append("has a high energy level")
    elif float(track["energy"]) <= 0.35:
        reasons.append("has a calmer sound")

    if float(track["danceability"]) >= 0.70 and track_mood != selected_mood:
        reasons.append("has strong danceability")

    if int(track["popularity"]) >= 75:
        reasons.append("is a popular track in the dataset")

    if int(track["release_year"]) >= 2018:
        reasons.append("is a relatively recent release")

    if not reasons:
        reasons.append("has the closest overall similarity to your current session choices")

    selected_reasons = reasons[:3]

    return "Recommended because it " + ", ".join(selected_reasons) + "."