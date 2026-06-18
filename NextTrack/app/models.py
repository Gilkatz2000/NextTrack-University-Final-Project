from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    genres: List[str]
    mood: str
    seed_artists: List[str]