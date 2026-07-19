import pandas as pd

df = pd.read_csv("../../data/processed/labeled.csv")

df["description"] = df["description"].fillna("")
df = df[df["views"] > 0]

df.to_csv("../../data/processed/clean.csv", index=False)

print("✅ Clean Done")