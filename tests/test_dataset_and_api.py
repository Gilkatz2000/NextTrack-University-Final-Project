from fastapi.testclient import TestClient

from app.data_loader import load_tracks
from app.main import app


client = TestClient(app)


REQUIRED_DATASET_COLUMNS = {
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
}


def test_dataset_loads_with_expected_size():
    df = load_tracks()

    assert len(df) >= 200


def test_dataset_has_required_columns():
    df = load_tracks()

    assert REQUIRED_DATASET_COLUMNS.issubset(set(df.columns))


def test_tracks_options_endpoint_returns_available_options():
    response = client.get("/tracks/options")

    assert response.status_code == 200

    data = response.json()

    assert "genres" in data
    assert "moods" in data
    assert "artists" in data

    assert isinstance(data["genres"], list)
    assert isinstance(data["moods"], list)
    assert isinstance(data["artists"], list)

    assert len(data["genres"]) > 0
    assert len(data["moods"]) > 0
    assert len(data["artists"]) > 0


def test_recommend_endpoint_returns_expanded_recommendation_fields():
    payload = {
        "genres": ["rock"],
        "mood": "energetic",
        "seed_artists": ["Arctic Monkeys"],
    }

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "recommendations" in data
    assert len(data["recommendations"]) > 0

    recommendation = data["recommendations"][0]

    for field in REQUIRED_DATASET_COLUMNS:
        assert field in recommendation

    assert "score" in recommendation
    assert "reason" in recommendation