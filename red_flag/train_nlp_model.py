# train_nlp_model.py
# Run this once to train and save the NLP red flag models
# Usage: python train_nlp_model.py

import pandas as pd
import numpy as np
import re
import joblib
import os
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score

# ── LOAD DATA ────────────────────────────────────────────────────────────────
# Put red_flag_dataset_advanced.xlsx in red_flag/ folder
df = pd.read_excel(r"C:\Users\dagaa\OneDrive\Desktop\lielow\red_flag\red_flag_dataset_advanced.xlsx")
df.columns = df.columns.str.strip().str.lower()
df = df[["scenario", "flag"]]

print("✅ Dataset loaded:", df.shape)
print(df.head())

# ── LABEL ────────────────────────────────────────────────────────────────────
df["flag"] = df["flag"].map({"red flag": 1, "green flag": 0})
df = df.dropna(subset=["flag"])
print("\nClass distribution:")
print(df["flag"].value_counts())

# ── CLEAN TEXT ───────────────────────────────────────────────────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def add_noise(text):
    words = text.split()
    if len(words) > 3:
        words.pop(random.randint(0, len(words) - 1))
    return " ".join(words)

df["scenario"] = df["scenario"].apply(clean_text)
df["scenario"] = df["scenario"].apply(lambda x: add_noise(x) if random.random() < 0.3 else x)

# ── VECTORIZE ────────────────────────────────────────────────────────────────
X = df["scenario"]
y = df["flag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ── TRAIN MODELS ─────────────────────────────────────────────────────────────
print("\n🏟 MODEL ARENA\n")

nb = MultinomialNB()
nb.fit(X_train_vec, y_train)
acc_nb = accuracy_score(y_test, nb.predict(X_test_vec))
f1_nb  = f1_score(y_test, nb.predict(X_test_vec))
print(f"Naive Bayes       | Accuracy: {acc_nb:.4f} | F1: {f1_nb:.4f}")

lr = LogisticRegression(C=0.5, max_iter=200)
lr.fit(X_train_vec, y_train)
acc_lr = accuracy_score(y_test, lr.predict(X_test_vec))
f1_lr  = f1_score(y_test, lr.predict(X_test_vec))
print(f"Logistic Regression| Accuracy: {acc_lr:.4f} | F1: {f1_lr:.4f}")

svm = SVC(probability=True)
svm.fit(X_train_vec, y_train)
acc_svm = accuracy_score(y_test, svm.predict(X_test_vec))
f1_svm  = f1_score(y_test, svm.predict(X_test_vec))
print(f"SVM               | Accuracy: {acc_svm:.4f} | F1: {f1_svm:.4f}")

# ── SAVE ─────────────────────────────────────────────────────────────────────
os.makedirs("red_flag/models", exist_ok=True)

joblib.dump(vectorizer, "red_flag/models/vectorizer.pkl")
joblib.dump(nb,         "red_flag/models/nb.pkl")
joblib.dump(lr,         "red_flag/models/lr.pkl")
joblib.dump(svm,        "red_flag/models/svm.pkl")
joblib.dump({
    "f1_nb":  f1_nb,  "acc_nb":  acc_nb,
    "f1_lr":  f1_lr,  "acc_lr":  acc_lr,
    "f1_svm": f1_svm, "acc_svm": acc_svm
}, "red_flag/models/scores.pkl")

print("\n✅ All models saved to red_flag/models/")
print("Files saved:")
for f in os.listdir("red_flag/models"):
    print(f"  - {f}")
