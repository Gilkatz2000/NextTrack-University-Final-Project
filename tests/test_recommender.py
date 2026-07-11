from collections import Counter

from app.recommender import get_recommendations

REQUIRED_RECOMMENDATION_FIELDS = {
    "track",
    "artist",
    "genre",
    "mood",
    "tempo",
    "energy",
    "popularity",
    "danceability",
    "valence",
    "release_year",
    "score",
    "reason",
    "spotify_url",
    "youtube_url",
}


def test_get_recommendations_returns_limited_list_with_expected_fields():
    recommendations = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=[
            "Arctic Monkeys"
        ],
        limit=5,
    )

    assert isinstance(
        recommendations,
        list,
    )

    assert (
        0
        < len(recommendations)
        <= 5
    )

    for item in recommendations:
        assert (
            set(item.keys())
            == REQUIRED_RECOMMENDATION_FIELDS
        )

        assert item[
            "spotify_url"
        ].startswith(
            "https://open.spotify.com/search/"
        )

        assert item[
            "youtube_url"
        ].startswith(
            "https://www.youtube.com/results?search_query="
        )

        assert (
            "official+audio"
            in item["youtube_url"]
        )


def test_recommendations_are_sorted_by_score_descending_after_filtering():
    recommendations = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=[
            "Arctic Monkeys"
        ],
        limit=5,
    )

    scores = [
        item["score"]
        for item in recommendations
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_recommendations_are_case_insensitive():
    lowercase_results = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=[
            "arctic monkeys"
        ],
        limit=5,
    )

    mixed_case_results = get_recommendations(
        genres=["Rock"],
        mood="Energetic",
        seed_artists=[
            "Arctic Monkeys"
        ],
        limit=5,
    )

    assert (
        lowercase_results
        == mixed_case_results
    )


def test_diversity_rules_limit_artist_and_genre_repetition():
    recommendations = get_recommendations(
        genres=[
            "rock",
            "indie rock",
        ],
        mood="energetic",
        seed_artists=[
            "The Strokes",
            "Arctic Monkeys",
        ],
        limit=5,
    )

    artist_counts = Counter(
        item["artist"]
        for item in recommendations
    )

    genre_counts = Counter(
        item["genre"]
        for item in recommendations
    )

    assert (
        max(
            artist_counts.values()
        )
        <= 1
    )

    assert (
        max(
            genre_counts.values()
        )
        <= 5
    )


def test_unknown_inputs_do_not_crash_and_still_return_recommendations():
    recommendations = get_recommendations(
        genres=[
            "unknown genre"
        ],
        mood="unknown mood",
        seed_artists=[
            "unknown artist"
        ],
        limit=5,
    )

    assert isinstance(
        recommendations,
        list,
    )

    assert len(
        recommendations
    ) > 0


def test_recommendation_contains_reason():
    recommendations = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=[
            "Arctic Monkeys"
        ],
        limit=5,
    )

    for recommendation in recommendations:
        assert (
            "reason"
            in recommendation
        )

        assert (
            recommendation["reason"]
            != ""
        )


def test_multiple_selected_genres_are_represented():
    recommendations = get_recommendations(
        genres=[
            "disco",
            "funk",
            "indie",
        ],
        mood="calm",
        seed_artists=[],
        limit=10,
    )

    returned_genres = {
        item["genre"]
        for item in recommendations
    }

    assert len(
        recommendations
    ) == 10

    assert (
        len(returned_genres)
        >= 2
    )


def test_soft_diversity_limits_genre_concentration_without_fixed_quotas():
    recommendations = get_recommendations(
        genres=[
            "disco",
            "funk",
            "indie",
        ],
        mood="calm",
        seed_artists=[],
        limit=10,
    )

    genre_counts = Counter(
        item["genre"]
        for item in recommendations
    )

    assert len(
        recommendations
    ) == 10

    assert (
        max(
            genre_counts.values()
        )
        <= 6
    )


def test_recommendations_do_not_repeat_artists():
    recommendations = get_recommendations(
        genres=[
            "rock",
            "pop",
            "hip hop",
        ],
        mood="energetic",
        seed_artists=[],
        limit=10,
    )

    artists = [
        item["artist"].lower()
        for item in recommendations
    ]

    assert len(
        artists
    ) == len(
        set(artists)
    )


def test_recommendations_do_not_repeat_tracks():
    recommendations = get_recommendations(
        genres=[
            "soul",
            "r&b",
            "electronic",
        ],
        mood="chill",
        seed_artists=[],
        limit=10,
    )

    track_keys = [
        (
            item["track"]
            .strip()
            .lower(),
            item["artist"]
            .strip()
            .lower(),
        )
        for item in recommendations
    ]

    assert len(
        track_keys
    ) == len(
        set(track_keys)
    )


def test_final_results_remain_sorted_after_soft_diversity_selection():
    recommendations = get_recommendations(
        genres=[
            "disco",
            "funk",
            "indie",
        ],
        mood="happy",
        seed_artists=[],
        limit=10,
    )

    scores = [
        item["score"]
        for item in recommendations
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_custom_recommendation_limit_is_respected():
    recommendations = get_recommendations(
        genres=[
            "synthpop",
            "electronic",
        ],
        mood="cool",
        seed_artists=[],
        limit=6,
    )

    assert len(
        recommendations
    ) == 6


def test_artist_display_capitalization_is_preserved():
    recommendations = get_recommendations(
        genres=["indie"],
        mood="energetic",
        seed_artists=[
            "TV On The Radio"
        ],
        limit=10,
    )

    matching_artists = [
        item["artist"]
        for item in recommendations
        if (
            item["artist"].lower()
            == "tv on the radio"
        )
    ]

    if matching_artists:
        assert (
            matching_artists[0]
            == "TV On The Radio"
        )


def test_genre_match_explanation_discloses_mood_difference():
    recommendations = get_recommendations(
        genres=["disco"],
        mood="energetic",
        seed_artists=[],
        limit=10,
    )

    mismatched_tracks = [
        item
        for item in recommendations
        if (
            item["genre"]
            == "disco"
            and item["mood"]
            != "energetic"
        )
    ]

    assert mismatched_tracks

    for item in mismatched_tracks:
        assert (
            "labelled mood differs"
            in item["reason"]
        )


def test_mood_profiles_change_the_audio_character_of_results():
    happy_results = get_recommendations(
        genres=[
            "pop",
            "indie",
        ],
        mood="happy",
        seed_artists=[],
        limit=10,
    )

    sad_results = get_recommendations(
        genres=[
            "pop",
            "indie",
        ],
        mood="sad",
        seed_artists=[],
        limit=10,
    )

    happy_average_valence = (
        sum(
            item["valence"]
            for item
            in happy_results
        )
        / len(happy_results)
    )

    sad_average_valence = (
        sum(
            item["valence"]
            for item
            in sad_results
        )
        / len(sad_results)
    )

    assert (
        happy_average_valence
        > sad_average_valence
    )

def test_seed_artist_measurably_influences_ranking():
    selected_artist = "A Tribe Called Quest"

    without_seed = get_recommendations(
        genres=["hip hop"],
        mood="cool",
        seed_artists=[],
        limit=10,
    )

    with_seed = get_recommendations(
        genres=["hip hop"],
        mood="cool",
        seed_artists=[
            selected_artist
        ],
        limit=10,
    )

    without_seed_results = {
        (
            recommendation["track"],
            recommendation["artist"],
        ): recommendation["score"]
        for recommendation in without_seed
    }

    with_seed_results = {
        (
            recommendation["track"],
            recommendation["artist"],
        ): recommendation["score"]
        for recommendation in with_seed
    }

    shared_tracks = (
        set(without_seed_results)
        & set(with_seed_results)
    )

    rankings_changed = (
        list(without_seed_results)
        != list(with_seed_results)
    )

    shared_scores_changed = any(
        with_seed_results[track_key]
        != without_seed_results[track_key]
        for track_key in shared_tracks
    )

    assert (
        rankings_changed
        or shared_scores_changed
    )

def test_richer_explanations_reference_audio_or_artist_similarity():
    recommendations = get_recommendations(
        genres=["hip hop"],
        mood="cool",
        seed_artists=[
            "A Tribe Called Quest"
        ],
        limit=10,
    )

    contains_richer_explanation = any(
        (
            "audio characteristics similar"
            in item["reason"]
        )
        or (
            "mood profile"
            in item["reason"]
        )
        or (
            "selected mood"
            in item["reason"]
        )
        for item in recommendations
    )

    assert contains_richer_explanation

def test_single_genre_session_prioritises_selected_genre():
    recommendations = get_recommendations(
        genres=["soul"],
        mood="calm",
        seed_artists=[],
        limit=10,
    )

    selected_genre_count = sum(
        1
        for recommendation
        in recommendations
        if recommendation["genre"]
        == "soul"
    )

    assert selected_genre_count >= 7