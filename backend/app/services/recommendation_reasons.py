def build_recommendation_reason(track, genres, mood, seed_artists):
    reasons = []

    track_genre = str(track["genre"]).strip().lower()
    track_mood = str(track["mood"]).strip().lower()
    track_artist = str(track["artist"]).strip().lower()

    selected_genres = [
        str(genre).strip().lower()
        for genre in genres
    ]
    selected_mood = str(mood).strip().lower()
    selected_artists = [
        str(artist).strip().lower()
        for artist in seed_artists
    ]

    genre_matches = track_genre in selected_genres
    mood_matches = track_mood == selected_mood

    tempo = float(track["tempo"])
    energy = float(track["energy"])
    popularity = int(track["popularity"])
    danceability = float(track["danceability"])
    valence = float(track["valence"])
    release_year = int(track["release_year"])

    if genre_matches and mood_matches:
        reasons.append(
            "matches both your selected genre and mood"
        )

    elif genre_matches:
        if selected_mood == "energetic" and energy >= 0.75:
            reasons.append(
                "is a strong genre match with energetic audio features, "
                "although its labelled mood differs from your selection"
            )

        elif (
            selected_mood in {"party", "happy"}
            and danceability >= 0.70
        ):
            reasons.append(
                "is a strong genre match with danceable audio features, "
                "although its labelled mood differs from your selection"
            )

        elif selected_mood == "calm" and energy <= 0.45:
            reasons.append(
                "is a strong genre match with calmer audio features, "
                "although its labelled mood differs from your selection"
            )

        else:
            reasons.append(
                "matches your selected genre, although its labelled mood "
                "differs from your selection"
            )

    elif mood_matches:
        reasons.append(
            "matches your selected mood and adds variety to your "
            "recommendations"
        )

    if track_artist in selected_artists:
        reasons.append(
            "uses an artist you already like"
        )

    # Choose one audio-feature explanation that is relevant to the
    # selected mood. This prevents the same high-energy explanation
    # appearing repeatedly.
    if selected_mood == "happy":
        if valence >= 0.75:
            reasons.append(
                "has a positive musical feel"
            )
        elif danceability >= 0.75:
            reasons.append(
                "has strong danceability"
            )
        elif energy >= 0.80:
            reasons.append(
                "has a high energy level"
            )

    elif selected_mood == "energetic":
        if energy >= 0.80:
            reasons.append(
                "has a high energy level"
            )
        elif tempo >= 120:
            reasons.append(
                "has an upbeat tempo"
            )
        elif danceability >= 0.75:
            reasons.append(
                "has strong danceability"
            )

    elif selected_mood == "party":
        if danceability >= 0.75:
            reasons.append(
                "has strong danceability"
            )
        elif energy >= 0.80:
            reasons.append(
                "has a high energy level"
            )
        elif tempo >= 120:
            reasons.append(
                "has an upbeat tempo"
            )

    elif selected_mood == "calm":
        if energy <= 0.40:
            reasons.append(
                "has a calmer sound"
            )
        elif tempo <= 95:
            reasons.append(
                "has a relaxed tempo"
            )
        elif valence >= 0.65:
            reasons.append(
                "has a warm musical feel"
            )

    elif selected_mood == "sad":
        if valence <= 0.40:
            reasons.append(
                "has a more reflective musical feel"
            )
        elif energy <= 0.45:
            reasons.append(
                "has a softer sound"
            )
        elif tempo <= 95:
            reasons.append(
                "has a slower tempo"
            )

    else:
        if energy >= 0.80:
            reasons.append(
                "has a high energy level"
            )
        elif energy <= 0.35:
            reasons.append(
                "has a calmer sound"
            )
        elif danceability >= 0.75:
            reasons.append(
                "has strong danceability"
            )

    if popularity >= 75:
        reasons.append(
            "is a popular track in the dataset"
        )

    if release_year >= 2018:
        reasons.append(
            "is a relatively recent release"
        )

    if not reasons:
        reasons.append(
            "has the closest overall similarity to your current "
            "session choices"
        )

    return (
        "Recommended because it "
        + ", ".join(reasons[:3])
        + "."
    )