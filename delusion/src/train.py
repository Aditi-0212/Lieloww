import pandas as pd
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


# =========================
# 1. LOAD DATASET
# =========================
df = pd.read_csv("C:/Users/dagaa/OneDrive/Desktop/New folder/data/final_cleaned_dataset.csv")

print("Dataset Loaded")
print(df.shape)


# =========================
# 2. NORMALIZE LABELS
# =========================
def normalize_label(label):
    label = str(label).lower()
    
    if "delusional" in label or "overconfident" in label:
        return "delusional"
    else:
        return "realistic"

df['final_label'] = df['final_label'].apply(normalize_label)

print("\nLabel Distribution:")
print(df['final_label'].value_counts())


# =========================
# 3. CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

df['clean_text'] = df['text'].apply(clean_text)


# =========================
# 4. SPLIT DATA
# =========================
X = df['clean_text']
y = df['final_label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# 5. TF-IDF
# =========================
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# =========================
# 6. TRAIN MODEL
# =========================
model = LogisticRegression(class_weight='balanced')

model.fit(X_train_tfidf, y_train)


# =========================
# 7. EVALUATION
# =========================
y_pred = model.predict(X_test_tfidf)

print("\nModel Performance:\n")
print(classification_report(y_test, y_pred))


# =========================
# 8. SAVE MODEL
# =========================
pickle.dump(model, open("../models/classifier.pkl", "wb"))
pickle.dump(vectorizer, open("../models/vectorizer.pkl", "wb"))
print("\nModel and vectorizer saved successfully!")