from typing import List

from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    genres: List[str]
    mood: str
    seed_artists: List[str]