import os

import pandas as pd
from qhchina import load_stopwords
from qhchina.analytics.collocations import find_collocates

TARGET_WORD = "他"
INPUT_FILE = "sentences.txt"
OUTPUT_DIR = "output"
MAX_P = 0.05
MIN_WORD_LENGTH = 2

RUNS = [
    {"name": "collocates_ta_window_h5", "method": "window", "horizon": 5},
    {"name": "collocates_ta_window_h10", "method": "window", "horizon": 10},
    {"name": "collocates_ta_sentence", "method": "sentence", "horizon": None},
]


def load_sentences(path):
    with open(path, encoding="utf-8") as f:
        return [line.split() for line in f if line.strip()]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sentences = load_sentences(INPUT_FILE)
    stopwords = load_stopwords()
    filters = {
        "max_p": MAX_P,
        "stopwords": list(stopwords),
        "min_word_length": MIN_WORD_LENGTH,
    }

    for run in RUNS:
        df = find_collocates(
            sentences,
            TARGET_WORD,
            method=run["method"],
            horizon=run["horizon"],
            filters=filters,
        )
        df = df.sort_values("obs_local", ascending=False).reset_index(drop=True)
        out_path = os.path.join(OUTPUT_DIR, run["name"] + ".csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\n=== {run['name']} ({run['method']}, horizon={run['horizon']}) "
              f"-> {out_path} ({len(df)} rows) ===")
        print(df.head(20).to_string())


if __name__ == "__main__":
    main()