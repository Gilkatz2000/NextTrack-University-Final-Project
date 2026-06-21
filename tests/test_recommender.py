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
    "spotify_url",
    "score",
    "reason",
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
    assert max(genre_counts.values()) <= 3


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