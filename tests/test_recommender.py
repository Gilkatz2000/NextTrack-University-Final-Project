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
        seed_artists=["Arctic Monkeys"],
        limit=5,
    )

    assert isinstance(recommendations, list)
    assert 0 < len(recommendations) <= 5
    for item in recommendations:
        assert set(item.keys()) == REQUIRED_RECOMMENDATION_FIELDS
        assert item["spotify_url"].startswith("https://open.spotify.com/search/")
        assert item["youtube_url"].startswith(
            "https://www.youtube.com/results?search_query="
        )
        assert "official+audio" in item["youtube_url"]


def test_recommendations_are_sorted_by_score_descending_after_filtering():
    recommendations = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=["Arctic Monkeys"],
        limit=5,
    )

    scores = [item["score"] for item in recommendations]
    assert scores == sorted(scores, reverse=True)


def test_recommendations_are_case_insensitive():
    lower_case = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=["arctic monkeys"],
        limit=5,
    )
    mixed_case = get_recommendations(
        genres=["Rock"],
        mood="Energetic",
        seed_artists=["Arctic Monkeys"],
        limit=5,
    )

    assert lower_case == mixed_case


def test_diversity_rules_limit_artist_and_genre_repetition():
    recommendations = get_recommendations(
        genres=["rock", "indie rock"],
        mood="energetic",
        seed_artists=["The Strokes", "Arctic Monkeys"],
        limit=5,
    )

    artist_counts = Counter(item["artist"] for item in recommendations)
    genre_counts = Counter(item["genre"] for item in recommendations)

    assert max(artist_counts.values()) <= 2
    assert max(genre_counts.values()) <= 6


def test_unknown_inputs_do_not_crash_and_still_return_recommendations():
    recommendations = get_recommendations(
        genres=["unknown genre"],
        mood="unknown mood",
        seed_artists=["unknown artist"],
        limit=5,
    )

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0

def test_recommendation_contains_reason():
    recommendations = get_recommendations(
        genres=["rock"],
        mood="energetic",
        seed_artists=["Arctic Monkeys"],
        limit=5,
    )

    for recommendation in recommendations:
        assert "reason" in recommendation
        assert recommendation["reason"] != ""

def test_multiple_selected_genres_are_represented():
    recommendations = get_recommendations(
        genres=["disco", "funk", "indie"],
        mood="calm",
        seed_artists=[],
        limit=10,
    )

    returned_genres = {item["genre"] for item in recommendations}

    assert len(recommendations) == 10
    assert "disco" in returned_genres
    assert "funk" in returned_genres
    assert "indie" in returned_genres


def test_selected_genres_are_reasonably_balanced():
    recommendations = get_recommendations(
        genres=["disco", "funk", "indie"],
        mood="calm",
        seed_artists=[],
        limit=10,
    )

    genre_counts = {}

    for item in recommendations:
        genre = item["genre"]
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    selected_counts = [
        genre_counts.get("disco", 0),
        genre_counts.get("funk", 0),
        genre_counts.get("indie", 0),
    ]

    assert max(selected_counts) - min(selected_counts) <= 1


def test_recommendations_do_not_repeat_artists():
    recommendations = get_recommendations(
        genres=["rock", "pop", "hip hop"],
        mood="energetic",
        seed_artists=[],
        limit=10,
    )

    artists = [item["artist"].lower() for item in recommendations]

    assert len(artists) == len(set(artists))


def test_recommendations_do_not_repeat_tracks():
    recommendations = get_recommendations(
        genres=["soul", "r&b", "electronic"],
        mood="chill",
        seed_artists=[],
        limit=10,
    )

    track_keys = [
        (
            item["track"].strip().lower(),
            item["artist"].strip().lower(),
        )
        for item in recommendations
    ]

    assert len(track_keys) == len(set(track_keys))


def test_no_three_consecutive_recommendations_share_a_genre():
    recommendations = get_recommendations(
        genres=["disco", "funk", "indie"],
        mood="happy",
        seed_artists=[],
        limit=10,
    )

    genres = [item["genre"] for item in recommendations]

    for index in range(len(genres) - 2):
        assert not (
            genres[index]
            == genres[index + 1]
            == genres[index + 2]
        )


def test_custom_recommendation_limit_is_respected():
    recommendations = get_recommendations(
        genres=["synthpop", "electronic"],
        mood="cool",
        seed_artists=[],
        limit=6,
    )

    assert len(recommendations) == 6

def test_artist_display_capitalization_is_preserved():
    recommendations = get_recommendations(
        genres=["indie"],
        mood="energetic",
        seed_artists=["TV On The Radio"],
        limit=10,
    )

    matching_artists = [
        item["artist"]
        for item in recommendations
        if item["artist"].lower() == "tv on the radio"
    ]

    if matching_artists:
        assert matching_artists[0] == "TV On The Radio"


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
        if item["genre"] == "disco"
        and item["mood"] != "energetic"
    ]

    assert mismatched_tracks

    for item in mismatched_tracks:
        assert "labelled mood differs" in item["reason"]