import csv

from frontend.feedback import FEEDBACK_COLUMNS, save_feedback


def test_save_feedback_creates_csv_with_expected_columns(tmp_path):
    feedback_file = tmp_path / "user_feedback.csv"

    save_feedback(
        genres=["rock", "pop"],
        mood="happy",
        artist="Coldplay",
        match_rating=4,
        diversity_rating=5,
        usability_rating=5,
        overall_rating=4,
        comments="Good recommendations",
        feedback_file=feedback_file,
    )

    assert feedback_file.exists()

    with feedback_file.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert reader.fieldnames == FEEDBACK_COLUMNS
    assert len(rows) == 1
    assert rows[0]["genres"] == "rock, pop"
    assert rows[0]["mood"] == "happy"
    assert rows[0]["artist"] == "Coldplay"
    assert rows[0]["match_rating"] == "4"
    assert rows[0]["comments"] == "Good recommendations"