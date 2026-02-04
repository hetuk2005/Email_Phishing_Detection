import pandas as pd
import re
import nltk
import os

from nltk.corpus import stopwords

# Download stopwords if not present
nltk.download("stopwords")

print("Current working directory:", os.getcwd())

# =========================
# LOAD DATASET SAFELY
# =========================
data = pd.read_csv("Dataset/emails.csv", low_memory=False)

print("Columns in dataset:")
print(data.columns)

# =========================
# TEXT CLEANING FUNCTION
# =========================
def clean_text(text):
    # Handle NaN or non-string safely
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)   # remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)      # remove special characters
    text = re.sub(r"\s+", " ", text).strip()     # remove extra spaces

    return text

# =========================
# APPLY CLEANING (SAFE)
# =========================
# Kaggle dataset already has 'text'
data["text"] = data["text"].fillna("").apply(clean_text)

# =========================
# OPTIONAL: SAVE CLEANED DATA
# =========================
# You can skip saving if you want
data.to_csv("Dataset/emails_cleaned.csv", index=False)

print("\n✅ Preprocessing completed successfully")
print("✅ Cleaned file saved as Dataset/emails_cleaned.csv")
