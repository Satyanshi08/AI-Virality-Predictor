import pandas as pd
import re

def extract_advanced_features(df):

    def row_feat(row):
        text = str(row["title"]) + " " + str(row["description"])

        emotional = len(re.findall(r"(amazing|wow|shocking)", text.lower()))
        numbers = len(re.findall(r"\d+", text))
        curiosity = len(re.findall(r"(wait for it|you won't believe)", text.lower()))

        title_len = len(row["title"])
        caps = sum(1 for c in row["title"] if c.isupper())
        caps_ratio = caps / title_len if title_len else 0

        tag_count = len(str(row["tags"]).split("|"))

        return pd.Series([
            emotional, numbers, curiosity,
            title_len, caps_ratio, tag_count,
            row["views"], row["likes"], row["comment_count"],
            row["category_id"]
        ])

    df[[
        "emotional","numbers","curiosity",
        "title_len","caps_ratio","tag_count",
        "views","likes","comment_count","category_id"
    ]] = df.apply(row_feat, axis=1)

    return df