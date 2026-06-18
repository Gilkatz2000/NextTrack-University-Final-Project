from app.recommender import get_recommendations
from app.baseline import get_baseline_recommendations

session = {
    "genres": ["rock"],
    "mood": "energetic",
    "seed_artists": ["Arctic Monkeys"]
}

print("\nNEXTTRACK\n")

recommendations = get_recommendations(
    session["genres"],
    session["mood"],
    session["seed_artists"]
)

for song in recommendations:
    print(song["track"], "-", song["artist"])

print("\nBASELINE\n")

baseline_recommendations = get_baseline_recommendations(session)

for song in baseline_recommendations:
    print(song["track"], "-", song["artist"])