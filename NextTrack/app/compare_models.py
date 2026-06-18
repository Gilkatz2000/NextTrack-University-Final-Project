import csv
import time
from collections import Counter

from app.baseline import get_baseline_recommendations
from app.recommender import get_recommendations


session = {
    "genres": ["rock"],
    "mood": "energetic",
    "seed_artists": ["Arctic Monkeys"]
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


def save_comparison_to_csv(nexttrack_metrics, baseline_metrics):
    rows = [
        {
            "metric": "Recommendations Returned",
            "nexttrack": nexttrack_metrics["recommendations_returned"],
            "baseline": baseline_metrics["recommendations_returned"],
        },
        {
            "metric": "Unique Artists",
            "nexttrack": nexttrack_metrics["unique_artists"],
            "baseline": baseline_metrics["unique_artists"],
        },
        {
            "metric": "Unique Genres",
            "nexttrack": nexttrack_metrics["unique_genres"],
            "baseline": baseline_metrics["unique_genres"],
        },
        {
            "metric": "Max Artist Repetition",
            "nexttrack": nexttrack_metrics["max_artist_repetition"],
            "baseline": baseline_metrics["max_artist_repetition"],
        },
        {
            "metric": "Max Genre Repetition",
            "nexttrack": nexttrack_metrics["max_genre_repetition"],
            "baseline": baseline_metrics["max_genre_repetition"],
        },
        {
            "metric": "Response Time Seconds",
            "nexttrack": nexttrack_metrics["response_time_seconds"],
            "baseline": baseline_metrics["response_time_seconds"],
        },
    ]

    with open("model_comparison_metrics.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["metric", "nexttrack", "baseline"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    start = time.time()
    nexttrack_recommendations = get_recommendations(
        session["genres"],
        session["mood"],
        session["seed_artists"],
    )
    nexttrack_time = time.time() - start

    start = time.time()
    baseline_recommendations = get_baseline_recommendations(session)
    baseline_time = time.time() - start

    nexttrack_metrics = calculate_metrics(nexttrack_recommendations, nexttrack_time)
    baseline_metrics = calculate_metrics(baseline_recommendations, baseline_time)

    print("\nNEXTTRACK RECOMMENDATIONS\n")
    for song in nexttrack_recommendations:
        print(f'{song["track"]} - {song["artist"]}')

    print("\nBASELINE RECOMMENDATIONS\n")
    for song in baseline_recommendations:
        print(f'{song["track"]} - {song["artist"]}')

    print("\nCOMPARISON METRICS\n")
    print(f'NextTrack unique artists: {nexttrack_metrics["unique_artists"]}')
    print(f'Baseline unique artists: {baseline_metrics["unique_artists"]}')
    print(f'NextTrack max artist repetition: {nexttrack_metrics["max_artist_repetition"]}')
    print(f'Baseline max artist repetition: {baseline_metrics["max_artist_repetition"]}')
    print(f'NextTrack response time: {nexttrack_metrics["response_time_seconds"]}')
    print(f'Baseline response time: {baseline_metrics["response_time_seconds"]}')

    save_comparison_to_csv(nexttrack_metrics, baseline_metrics)
    print("\nComparison metrics saved to model_comparison_metrics.csv")


if __name__ == "__main__":
    main()