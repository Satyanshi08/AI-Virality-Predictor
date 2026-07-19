import pandas as pd
import os

def prepare():
    files = [
        "../../data/raw/USvideos.csv",
        "../../data/raw/INvideos.csv"
    ]

    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    df = df.dropna(subset=["title", "views", "likes", "comment_count"])

    os.makedirs("../../data/processed", exist_ok=True)
    df.to_csv("../../data/processed/final.csv", index=False)

    print("✅ Data Prepared")

if __name__ == "__main__":
    prepare()