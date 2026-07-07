import csv
import time
from collections import Counter

from app.recommender import get_recommendations
from app.test_sessions import TEST_SESSIONS


def calculate_relevance_metrics(recommendations, session):
    expected_genres = set(session["input"]["genres"])
    expected_mood = session["input"]["mood"]

    genre_matches = sum(
        1 for item in recommendations
        if item["genre"] in expected_genres
    )

    mood_matches = sum(
        1 for item in recommendations
        if item["mood"] == expected_mood
    )

    total = len(recommendations)

    return {
        "genre_match_count": genre_matches,
        "mood_match_count": mood_matches,
        "genre_match_rate": round(genre_matches / total, 2) if total else 0,
        "mood_match_rate": round(mood_matches / total, 2) if total else 0,
    }


def evaluate_session(session):
    start_time = time.time()

    recommendations = get_recommendations(
        genres=session["input"]["genres"],
        mood=session["input"]["mood"],
        seed_artists=session["input"]["seed_artists"],
        limit=5,
    )

    response_time = time.time() - start_time

    artist_counts = Counter(item["artist"] for item in recommendations)
    genre_counts = Counter(item["genre"] for item in recommendations)

    max_artist_repetition = max(artist_counts.values()) if artist_counts else 0
    max_genre_repetition = max(genre_counts.values()) if genre_counts else 0

    relevance_metrics = calculate_relevance_metrics(recommendations, session)

    return {
        "session_name": session["name"],
        "recommendation_count": len(recommendations),
        "response_time_seconds": round(response_time, 4),
        "max_artist_repetition": max_artist_repetition,
        "max_genre_repetition": max_genre_repetition,
        "genre_match_count": relevance_metrics["genre_match_count"],
        "mood_match_count": relevance_metrics["mood_match_count"],
        "genre_match_rate": relevance_metrics["genre_match_rate"],
        "mood_match_rate": relevance_metrics["mood_match_rate"],
        "passed_response_time": response_time < 1,
        "passed_artist_diversity": max_artist_repetition <= 2,
        "passed_genre_diversity": max_genre_repetition <= 6,
    }


def run_evaluation():
    return [evaluate_session(session) for session in TEST_SESSIONS]


def save_results_to_csv(results, filename="evaluation_results.csv"):
    fieldnames = [
        "session_name",
        "recommendation_count",
        "response_time_seconds",
        "max_artist_repetition",
        "max_genre_repetition",
        "genre_match_count",
        "mood_match_count",
        "genre_match_rate",
        "mood_match_rate",
        "passed_response_time",
        "passed_artist_diversity",
        "passed_genre_diversity",
    ]

    with open(filename, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    results = run_evaluation()

    for result in results:
        print(result)

    save_results_to_csv(results)
    print("\nEvaluation results saved to evaluation_results.csv")