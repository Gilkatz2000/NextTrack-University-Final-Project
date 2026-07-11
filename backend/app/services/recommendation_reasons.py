"""Human-readable explanations for NextTrack recommendations."""


def _feature_matches(
    track,
    mood_profile,
):
    """Return audio observations that are close to the selected mood profile."""

    observations = []

    energy = float(
        track["energy"]
    )

    danceability = float(
        track["danceability"]
    )

    valence = float(
        track["valence"]
    )

    # Approximate the same normalised range used by the recommender.
    # Dataset tempos are expected to remain approximately between 60 and 192 BPM.
    tempo_scaled = max(
        0.0,
        min(
            1.0,
            (
                float(track["tempo"])
                - 60.0
            )
            / 132.0,
        ),
    )

    comparisons = [
        (
            abs(
                energy
                - mood_profile["energy"]
            ),
            "energy",
            energy,
        ),
        (
            abs(
                danceability
                - mood_profile[
                    "danceability"
                ]
            ),
            "danceability",
            danceability,
        ),
        (
            abs(
                valence
                - mood_profile["valence"]
            ),
            "valence",
            valence,
        ),
        (
            abs(
                tempo_scaled
                - mood_profile["tempo"]
            ),
            "tempo",
            float(track["tempo"]),
        ),
    ]

    # Explain the two audio features closest to the selected mood profile.
    comparisons.sort(
        key=lambda item: item[0]
    )

    for distance, feature, value in comparisons:
        if distance > 0.18:
            continue

        if feature == "energy":
            if value >= 0.75:
                observations.append(
                    "its high energy supports the selected mood"
                )

            elif value <= 0.40:
                observations.append(
                    "its softer energy supports the selected mood"
                )

            else:
                observations.append(
                    "its balanced energy is close to the mood profile"
                )

        elif feature == "danceability":
            if value >= 0.72:
                observations.append(
                    "its strong danceability fits the mood profile"
                )

            elif value <= 0.42:
                observations.append(
                    "its restrained danceability fits the mood profile"
                )

            else:
                observations.append(
                    "its danceability is close to the mood profile"
                )

        elif feature == "valence":
            if value >= 0.70:
                observations.append(
                    "its positive musical tone fits the selected mood"
                )

            elif value <= 0.35:
                observations.append(
                    "its lower valence gives it a more reflective tone"
                )

            else:
                observations.append(
                    "its emotional tone is close to the mood profile"
                )

        elif feature == "tempo":
            if value >= 120:
                observations.append(
                    "its upbeat tempo fits the selected mood"
                )

            elif value <= 95:
                observations.append(
                    "its slower tempo fits the selected mood"
                )

            else:
                observations.append(
                    "its tempo is close to the mood profile"
                )

        if len(observations) == 2:
            break

    return observations


def _mood_contradictions(
    track,
    selected_mood,
):
    """Return important audio conflicts with the selected mood."""

    contradictions = []

    energy = float(
        track["energy"]
    )

    valence = float(
        track["valence"]
    )

    danceability = float(
        track["danceability"]
    )

    selected_mood = str(
        selected_mood
    ).strip().lower()

    if (
        selected_mood == "angry"
        and valence >= 0.70
    ):
        contradictions.append(
            "its very positive tone differs from the darker emotional profile of your selected mood"
        )

    elif (
        selected_mood
        in {
            "sad",
            "dark",
        }
        and valence >= 0.70
    ):
        contradictions.append(
            "its positive tone differs from your selected mood"
        )

    if (
        selected_mood == "calm"
        and energy >= 0.80
    ):
        contradictions.append(
            "its high energy is less typical of the selected mood"
        )

    if (
        selected_mood == "party"
        and danceability <= 0.40
    ):
        contradictions.append(
            "its lower danceability is less typical of a party track"
        )

    if (
        selected_mood == "energetic"
        and energy <= 0.40
    ):
        contradictions.append(
            "its softer energy is less typical of the selected mood"
        )

    return contradictions


def build_recommendation_reason(
    track,
    genres,
    mood,
    seed_artists,
    mood_profile=None,
):
    """Build an explanation using genre, mood, audio and artist similarity."""

    reasons = []

    track_genre = str(
        track["genre"]
    ).strip().lower()

    track_mood = str(
        track["mood"]
    ).strip().lower()

    track_artist = str(
        track["artist"]
    ).strip().lower()

    selected_genres = [
        str(genre).strip().lower()
        for genre in genres
    ]

    selected_mood = str(
        mood
    ).strip().lower()

    selected_artists = [
        str(artist).strip().lower()
        for artist in seed_artists
    ]

    genre_matches = (
        track_genre
        in selected_genres
    )

    mood_matches = (
        track_mood
        == selected_mood
    )

    if (
        genre_matches
        and mood_matches
    ):
        reasons.append(
            "matches both your selected genre and labelled mood"
        )

    elif genre_matches:
        reasons.append(
            "matches your selected genre"
        )

    elif mood_matches:
        reasons.append(
            "matches your selected mood while adding genre variety"
        )

    artist_similarity = float(
        track.get(
            "artist_similarity_score",
            0.0,
        )
    )

    if track_artist in selected_artists:
        reasons.append(
            "is by an artist you selected"
        )

    elif (
        selected_artists
        and artist_similarity >= 0.72
    ):
        reasons.append(
            "has audio characteristics similar to your selected artist"
        )

    if (
        not mood_matches
        and genre_matches
    ):
        mood_audio_score = float(
            track.get(
                "mood_audio_score",
                0.0,
            )
        )

        contradictions = _mood_contradictions(
            track,
            selected_mood,
        )

        if contradictions:
            reasons.append(
                "its labelled mood differs from your selection"
            )

            reasons.extend(
                contradictions
            )

        elif mood_audio_score >= 0.78:
            reasons.append(
                "its labelled mood differs, but some audio characteristics "
                "remain reasonably close to your selected mood"
            )

        else:
            reasons.append(
                "its labelled mood differs from your selection"
            )

    if mood_profile:
        feature_reasons = _feature_matches(
            track,
            mood_profile,
        )

        for feature_reason in feature_reasons:
            if len(reasons) >= 3:
                break

            reasons.append(
                feature_reason
            )

    popularity = int(
        track["popularity"]
    )

    if (
        popularity >= 85
        and len(reasons) < 3
    ):
        reasons.append(
            "it has a high popularity value"
        )

    if not reasons:
        reasons.append(
            "has the closest overall content similarity to this session"
        )

    # Remove repeated explanation phrases while preserving order.
    unique_reasons = []

    for reason in reasons:
        if reason not in unique_reasons:
            unique_reasons.append(
                reason
            )

    return (
        "Recommended because it "
        + ", ".join(
            unique_reasons[:3]
        )
        + "."
    )