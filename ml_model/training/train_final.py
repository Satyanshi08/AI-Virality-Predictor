import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from ml_model.feature_engineering.text_advanced import TFIDF
from ml_model.feature_engineering.advanced_features import extract_advanced_features

df = pd.read_csv("data/processed/clean.csv")


# 🔥 ADD THIS FIX
df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")
# 🔥 LIMIT DATA (VERY IMPORTANT)
df = df.sample(20000, random_state=42)

text = df["title"] + " " + df["description"]

df = extract_advanced_features(df)


tfidf = TFIDF()
text_feat = tfidf.fit_transform(text)

meta = df[[
    "emotional","numbers","curiosity",
    "title_len","caps_ratio","tag_count",
    "views","likes","comment_count","category_id"
]].values

scaler = StandardScaler()
meta = scaler.fit_transform(meta)

X = np.concatenate([text_feat, meta], axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = XGBClassifier(n_estimators=300, max_depth=7)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))
import os

os.makedirs("models", exist_ok=True)

pickle.dump(model, open("models/model.pkl", "wb"))
tfidf.save("models/tfidf.pkl")
pickle.dump(scaler, open("models/scaler.pkl", "wb"))
# 🔥 LIMIT DATA (VERY IMPORTANT)
