import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

# Load dataset
data = pd.read_csv('../dataset/emails.csv')

X = data['text']
y = data['label']

# Convert text to numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, '../model/spam_model.pkl')
joblib.dump(vectorizer, '../model/vectorizer.pkl')

# Test model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
