import os
print("Current working directory:", os.getcwd())
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords

nltk.download('stopwords')

# Load dataset
data = pd.read_csv('Dataset/emails.csv')

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

data['text'] = data['text'].apply(clean_text)

print("Preprocessing Done")
