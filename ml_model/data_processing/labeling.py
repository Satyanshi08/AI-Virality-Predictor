import pandas as pd

df = pd.read_csv("../../data/processed/final.csv")

df["engagement"] = (df["likes"] + df["comment_count"]) / df["views"]
df["score"] = df["views"] * df["engagement"]

threshold = df["score"].quantile(0.75)
df["label"] = (df["score"] > threshold).astype(int)

df.to_csv("../../data/processed/labeled.csv", index=False)

print("✅ Labeling Done")