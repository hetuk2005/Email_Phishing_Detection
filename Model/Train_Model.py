import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# =========================
# BASIC INFO
# =========================
print("Current working directory:", os.getcwd())

# =========================
# LOAD DATASET SAFELY
# =========================
data = pd.read_csv("Dataset/emails.csv", low_memory=False)

print("\nColumns in dataset:")
print(data.columns)

# =========================
# USE CLEAN TEXT + LABEL
# =========================
# Kaggle dataset already provides cleaned columns
X = data["text"]
y = data["label"]

# =========================
# CRITICAL DATA CLEANING
# =========================
# Remove rows where text or label is NaN
mask = X.notna() & y.notna()
X = X[mask]
y = y[mask]

# Convert to string AFTER NaN removal
X = X.astype(str)

# Remove empty / whitespace-only emails
mask2 = X.str.strip() != ""
X = X[mask2]
y = y[mask2]

print("\nTotal samples after cleaning:", len(X))
print("Label distribution:")
print(y.value_counts())

# =========================
# TRAIN–TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# TF-IDF VECTORIZATION
# =========================
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    token_pattern=r"(?u)\b\w+\b"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =========================
# MODEL TRAINING
# =========================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_vec, y_train)

# =========================
# EVALUATION
# =========================
y_pred = model.predict(X_test_vec)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL & VECTORIZER
# =========================
joblib.dump(model, "Spam_Model.pkl")
joblib.dump(vectorizer, "Vectorizer.pkl")

print("\n✅ Model training completed successfully")
print("✅ Model saved as Spam_Model.pkl")
print("✅ Vectorizer saved as Vectorizer.pkl")
