from app.data_loader import load_tracks


def get_baseline_recommendations(session, top_n=5):
    df = load_tracks()

    genres = [genre.lower() for genre in session.get("genres", [])]

    df["genre"] = df["genre"].str.lower()

    results = df[df["genre"].isin(genres)]

    results = results.sort_values(
        by="popularity",
        ascending=False
    )

    return results.head(top_n).to_dict("records")