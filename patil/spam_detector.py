import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("your_file.csv")

# Keep only required columns
df = df[['text', 'label']]

# Drop null values
df.dropna(inplace=True)

# =========================
# FEATURES & LABELS
# =========================
X = df['text']
y = df['label']

# =========================
# TEXT → NUMBERS
# =========================
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vec = vectorizer.fit_transform(X)

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

# =========================
# MODEL
# =========================
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================
y_pred = model.predict(X_test)

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))

# =========================
# PREDICTION FUNCTION
# =========================
def predict_email(text):
    vec = vectorizer.transform([text])
    result = model.predict(vec)[0]
    return "Spam/Phishing" if result == 1 else "Safe Email"

# =========================
# SIMPLE TEST INTERFACE
# =========================
while True:
    msg = input("\nEnter email (or 'exit'): ")
    if msg.lower() == "exit":
        break
    
    print("Result:", predict_email(msg))