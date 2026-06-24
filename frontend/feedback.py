import csv
from datetime import datetime
from pathlib import Path

FEEDBACK_FILE = Path("evaluation/user_feedback.csv")

FEEDBACK_COLUMNS = [
    "timestamp",
    "genres",
    "mood",
    "artist",
    "match_rating",
    "diversity_rating",
    "usability_rating",
    "overall_rating",
    "comments",
]


def save_feedback(
    genres,
    mood,
    artist,
    match_rating,
    diversity_rating,
    usability_rating,
    overall_rating,
    comments,
    feedback_file=FEEDBACK_FILE,
):
    feedback_file.parent.mkdir(exist_ok=True)

    file_exists = feedback_file.exists()

    with feedback_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FEEDBACK_COLUMNS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "genres": ", ".join(genres),
                "mood": mood,
                "artist": artist if artist else "No artist selected",
                "match_rating": match_rating,
                "diversity_rating": diversity_rating,
                "usability_rating": usability_rating,
                "overall_rating": overall_rating,
                "comments": comments,
            }
        )