import pickle
import numpy as np
import re

from ml_model.feature_engineering.text_advanced import TFIDF

# ✅ Load trained model
model = pickle.load(open("models/model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# ✅ Load TF-IDF
tfidf = TFIDF()
tfidf.load("models/tfidf.pkl")


# 🔥 Helper functions (same logic as training)

def extract_pattern_features(text):
    text = text.lower()

    emotional = len(re.findall(r"(amazing|wow|shocking)", text))
    numbers = len(re.findall(r"\d+", text))
    curiosity = len(re.findall(r"(wait for it|you won't believe)", text))

    return emotional, numbers, curiosity


def extract_metadata_features(data):
    title = data["title"]

    title_len = len(title)
    caps = sum(1 for c in title if c.isupper())
    caps_ratio = caps / title_len if title_len > 0 else 0

    tag_count = 5  # dummy (dataset me tha but input me nahi)

    return title_len, caps_ratio, tag_count


# 🔥 MAIN PREDICTION FUNCTION

def predict(data):
    # 🔹 Text features
    text = data["title"] + " " + data["description"]
    text_feat = tfidf.transform([text])[0]

    # 🔹 Pattern features
    emotional, numbers, curiosity = extract_pattern_features(text)

    # 🔹 Metadata features
    title_len, caps_ratio, tag_count = extract_metadata_features(data)

    # 🔹 Combine meta (IMPORTANT: SAME 10 FEATURES AS TRAINING)
    meta = np.array([[
        emotional,
        numbers,
        curiosity,
        title_len,
        caps_ratio,
        tag_count,
        data["views"],
        data["likes"],
        data["comment_count"],
        data["category_id"]
    ]])

    # 🔹 Scale
    meta = scaler.transform(meta)

    # 🔹 Final feature vector
    final = np.concatenate([text_feat, meta[0]])

    # 🔹 Prediction
    prob = model.predict_proba([final])[0][1]

    return {
        "prediction": "Viral" if prob > 0.5 else "Not Viral",
        "probability": float(prob)
    }