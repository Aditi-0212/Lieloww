# train_quiz_model.py
# Run this once to train and save the quiz models
# Usage: python train_quiz_model.py

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score

# ── LOAD DATA ────────────────────────────────────────────────────────────────
# Put redflag_sheet.xlsx in the same folder as this file
df = pd.read_excel(r"C:\Users\dagaa\OneDrive\Desktop\lielow\red_flag\redflag_sheet (1).xlsx")

print("✅ Dataset loaded:", df.shape)
print(df.head())

# ── CLEAN ────────────────────────────────────────────────────────────────────
df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

df.replace({"red flag": 1, "green flag": 0}, inplace=True)

columns = [
    "phone_checking_flag",
    "jealousy_flag",
    "career_support_flag",
    "apology_maturity_flag",
    "opposite_gender_bestfriend_flag"
]

df[columns] = df[columns].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=columns)

# ── AGREEMENT SCORE + LABELS ─────────────────────────────────────────────────
df["red_count"] = df[columns].sum(axis=1)
df["agreement_score"] = df["red_count"] / len(columns)

def label_row(row):
    if row["agreement_score"] >= 0.7:
        return 2   # Toxic
    elif row["agreement_score"] <= 0.3:
        return 0   # Healthy
    else:
        return 1   # Neutral

df["overall_flag"] = df.apply(label_row, axis=1)
print("\nClass distribution:")
print(df["overall_flag"].value_counts())

# ── TRAIN/TEST SPLIT ─────────────────────────────────────────────────────────
X = df[columns + ["agreement_score"]]
noise = np.random.normal(0, 0.1, X.shape)
X = X + noise
y = df["overall_flag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── MODEL ARENA ──────────────────────────────────────────────────────────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM":                 SVC(probability=True, C=0.5),
    "Random Forest":       RandomForestClassifier(max_depth=3, n_estimators=50),
    "KNN":                 KNeighborsClassifier(n_neighbors=7)
}

best_model = None
best_name = ""
best_f1 = 0

print("\n🏟 MODEL ARENA\n")
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    print(f"{name} | Accuracy: {acc:.4f} | F1: {f1:.4f}")
    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_name = name

print(f"\n🏆 Best Model: {best_name} (F1: {best_f1:.4f})")

# ── SAVE MODELS ──────────────────────────────────────────────────────────────
os.makedirs("red_flag/models", exist_ok=True)

joblib.dump(best_model, "red_flag/models/quiz_model.pkl")
joblib.dump(best_name,  "red_flag/models/quiz_model_name.pkl")

# save all models too (for arena display)
for name, model in models.items():
    safe_name = name.lower().replace(" ", "_")
    joblib.dump(model, f"red_flag/models/quiz_{safe_name}.pkl")

print("\n✅ Models saved to red_flag/models/")
print("Files saved:")
for f in os.listdir("red_flag/models"):
    print(f"  - {f}")
