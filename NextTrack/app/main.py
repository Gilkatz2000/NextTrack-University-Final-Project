from fastapi import FastAPI

from app.data_loader import load_tracks
from app.models import RecommendationRequest
from app.recommender import get_recommendations

app = FastAPI(title="NextTrack API")


@app.get("/")
def root():
    return {"message": "NextTrack API running"}


@app.post("/recommend")
def recommend(request: RecommendationRequest):
    recommendations = get_recommendations(
        genres=request.genres,
        mood=request.mood,
        seed_artists=request.seed_artists,
    )

    return {
        "session_input": request,
        "recommendations": recommendations,
    }


@app.get("/tracks/options")
def get_track_options():
    df = load_tracks()

    return {
        "genres": sorted(df["genre"].dropna().unique().tolist()),
        "moods": sorted(df["mood"].dropna().unique().tolist()),
        "artists": sorted(df["artist"].dropna().unique().tolist()),
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "NextTrack API",
    }