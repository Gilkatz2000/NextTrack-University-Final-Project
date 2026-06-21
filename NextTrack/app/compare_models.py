import csv
import time
from collections import Counter

from app.baseline import get_baseline_recommendations
from app.recommender import get_recommendations
from app.recommender_v2 import get_recommendations_v2


session = {
    "genres": ["rock"],
    "mood": "energetic",
    "seed_artists": ["Arctic Monkeys"],
}


def calculate_metrics(recommendations, response_time):
    artist_counts = Counter(song["artist"] for song in recommendations)
    genre_counts = Counter(song["genre"] for song in recommendations)

    return {
        "recommendations_returned": len(recommendations),
        "unique_artists": len(artist_counts),
        "unique_genres": len(genre_counts),
        "max_artist_repetition": max(artist_counts.values()) if artist_counts else 0,
        "max_genre_repetition": max(genre_counts.values()) if genre_counts else 0,
        "response_time_seconds": round(response_time, 4),
    }


def save_comparison_to_csv(baseline_metrics, v1_metrics, v2_metrics):
    rows = [
        {
            "metric": "Recommendations Returned",
            "baseline": baseline_metrics["recommendations_returned"],
            "nexttrack_v1": v1_metrics["recommendations_returned"],
            "nexttrack_v2": v2_metrics["recommendations_returned"],
        },
        {
            "metric": "Unique Artists",
            "baseline": baseline_metrics["unique_artists"],
            "nexttrack_v1": v1_metrics["unique_artists"],
            "nexttrack_v2": v2_metrics["unique_artists"],
        },
        {
            "metric": "Unique Genres",
            "baseline": baseline_metrics["unique_genres"],
            "nexttrack_v1": v1_metrics["unique_genres"],
            "nexttrack_v2": v2_metrics["unique_genres"],
        },
        {
            "metric": "Max Artist Repetition",
            "baseline": baseline_metrics["max_artist_repetition"],
            "nexttrack_v1": v1_metrics["max_artist_repetition"],
            "nexttrack_v2": v2_metrics["max_artist_repetition"],
        },
        {
            "metric": "Max Genre Repetition",
            "baseline": baseline_metrics["max_genre_repetition"],
            "nexttrack_v1": v1_metrics["max_genre_repetition"],
            "nexttrack_v2": v2_metrics["max_genre_repetition"],
        },
        {
            "metric": "Response Time Seconds",
            "baseline": baseline_metrics["response_time_seconds"],
            "nexttrack_v1": v1_metrics["response_time_seconds"],
            "nexttrack_v2": v2_metrics["response_time_seconds"],
        },
    ]

    with open("model_comparison_v2_metrics.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["metric", "baseline", "nexttrack_v1", "nexttrack_v2"],
        )
        writer.writeheader()
        writer.writerows(rows)


def time_function(function, *args):
    start = time.time()
    result = function(*args)
    response_time = time.time() - start

    return result, response_time


def print_recommendations(title, recommendations):
    print(f"\n{title}\n")

    for song in recommendations:
        print(f'{song["track"]} - {song["artist"]}')


def main():
    baseline_recommendations, baseline_time = time_function(
        get_baseline_recommendations,
        session,
    )

    v1_recommendations, v1_time = time_function(
        get_recommendations,
        session["genres"],
        session["mood"],
        session["seed_artists"],
    )

    v2_recommendations, v2_time = time_function(
        get_recommendations_v2,
        session["genres"],
        session["mood"],
        session["seed_artists"],
    )

    baseline_metrics = calculate_metrics(baseline_recommendations, baseline_time)
    v1_metrics = calculate_metrics(v1_recommendations, v1_time)
    v2_metrics = calculate_metrics(v2_recommendations, v2_time)

    print_recommendations("BASELINE RECOMMENDATIONS", baseline_recommendations)
    print_recommendations("NEXTTRACK V1 RECOMMENDATIONS", v1_recommendations)
    print_recommendations("NEXTTRACK V2 RECOMMENDATIONS", v2_recommendations)

    print("\nCOMPARISON METRICS\n")
    print(f'Baseline unique artists: {baseline_metrics["unique_artists"]}')
    print(f'NextTrack v1 unique artists: {v1_metrics["unique_artists"]}')
    print(f'NextTrack v2 unique artists: {v2_metrics["unique_artists"]}')
    print()
    print(f'Baseline max artist repetition: {baseline_metrics["max_artist_repetition"]}')
    print(f'NextTrack v1 max artist repetition: {v1_metrics["max_artist_repetition"]}')
    print(f'NextTrack v2 max artist repetition: {v2_metrics["max_artist_repetition"]}')
    print()
    print(f'Baseline response time: {baseline_metrics["response_time_seconds"]}')
    print(f'NextTrack v1 response time: {v1_metrics["response_time_seconds"]}')
    print(f'NextTrack v2 response time: {v2_metrics["response_time_seconds"]}')

    save_comparison_to_csv(baseline_metrics, v1_metrics, v2_metrics)
    print("\nComparison metrics saved to model_comparison_v2_metrics.csv")


if __name__ == "__main__":
    main()