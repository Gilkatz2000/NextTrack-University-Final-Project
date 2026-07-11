from pathlib import Path

import pandas as pd

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "tracks.csv"


def load_tracks():
    return pd.read_csv(DATASET_PATH)