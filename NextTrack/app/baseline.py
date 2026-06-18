import pandas as pd

DATASET_PATH = "NextTrack/app/dataset.csv"

def get_baseline_recommendations(session, top_n=5):
    df = pd.read_csv(DATASET_PATH)

    genres = session.get("genres", [])

    results = df[df["genre"].isin(genres)]

    results = results.sort_values(
        by="popularity",
        ascending=False
    )

    return results.head(top_n).to_dict("records")