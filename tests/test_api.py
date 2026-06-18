from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "NextTrack API",
    }


def test_recommend_endpoint_returns_session_input_and_recommendations():
    payload = {
        "genres": ["rock"],
        "mood": "energetic",
        "seed_artists": ["Arctic Monkeys"],
    }

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["session_input"] == payload
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0


def test_recommend_endpoint_rejects_invalid_request_body():
    response = client.post("/recommend", json={"genres": ["rock"]})

    assert response.status_code == 422