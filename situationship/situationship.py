
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

# -------------------------------
# STEP 1: CREATE SYNTHETIC DATASET
# -------------------------------
np.random.seed(42)

n_samples = 1000
data = []

for _ in range(n_samples):
    row = {
        "avoid_label": np.random.randint(0, 2),
        "cancels": np.random.randint(0, 2),
        "inconsistent_communication": np.random.randint(0, 2),
        "last_minute_plans": np.random.randint(0, 2),
        "mixed_signals": np.random.randint(0, 2),
        "emotional_imbalance": np.random.randint(0, 2),
        "lack_of_effort": np.random.randint(0, 2),
        "no_future_talk": np.random.randint(0, 2),
        "feels_one_sided": np.random.randint(0, 2),
        "avoids_serious_talk": np.random.randint(0, 2),
        "private_meet": np.random.randint(0, 2),
        "possessive_no_label": np.random.randint(0, 2),
        "talks_to_others": np.random.randint(0, 2),
        "hot_and_cold": np.random.randint(0, 2),
        "gaslighting": np.random.randint(0, 2)
    }

    score = sum(row.values())

    if score >= 9:
        label = 0
    elif score <= 5:
        label = 1
    else:
        label = np.random.choice([0, 1])

    row["Label"] = label
    data.append(row)

df = pd.DataFrame(data)

print("Dataset Created:", df.shape)

# -------------------------------
# FEATURES + TARGET
# -------------------------------
feature_cols = list(df.columns[:-1])

X = df[feature_cols]
y = df["Label"]

# -------------------------------
# TRAIN TEST SPLIT
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# MODELS
# -------------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(probability=True),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
}

trained_models = {}
accuracies = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    acc = round(model.score(X_test, y_test), 2)
    trained_models[name] = model
    accuracies[name] = acc

# -------------------------------
# USER INPUT
# -------------------------------
print("\nAnswer with Yes or No:\n")

def yn(q):
    return 1 if input(q + " ").strip().lower() == "yes" else 0

user_input = {
    "avoid_label": yn("Do they avoid labeling the relationship?"),
    "cancels": yn("Do they cancel plans often?"),
    "inconsistent_communication": yn("Is communication inconsistent?"),
    "last_minute_plans": yn("Do they make last minute plans?"),
    "mixed_signals": yn("Do they give mixed signals?"),
    "emotional_imbalance": yn("Is there emotional imbalance?"),
    "lack_of_effort": yn("Do they put in low effort?"),
    "no_future_talk": yn("Do they avoid talking about the future?"),
    "feels_one_sided": yn("Does it feel one-sided?"),
    "avoids_serious_talk": yn("Do they avoid serious conversations?"),
    "private_meet": yn("Do they only meet privately?"),
    "possessive_no_label": yn("Are they possessive without a label?"),
    "talks_to_others": yn("Are they actively talking to other people?"),
    "hot_and_cold": yn("Are they hot and cold?"),
    "gaslighting": yn("Do they manipulate or gaslight?")
}

input_df = pd.DataFrame([user_input])

# -------------------------------
# MODEL ARENA
# -------------------------------
print("\n--- Model Arena ---")

predictions = {}

for name, model in trained_models.items():
    pred = model.predict(input_df)[0]
    predictions[name] = pred

    print(f"{name}: {pred} (Accuracy: {accuracies[name]})")

# -------------------------------
# FINAL RESULT
# -------------------------------
votes = list(predictions.values())
final_pred = round(sum(votes) / len(votes))

print("\n--- Situationship Survival Result ---")

if final_pred == 1:
    print("The situationship will likely survive 💚")
else:
    print("The situationship will likely fail 💔")

# -------------------------------
# AGREEMENT
# -------------------------------
if len(set(votes)) == 1:
    print("\nAll models agree")
else:
    print("\nModels show variation")

# -------------------------------
# ARENA WINNER
# -------------------------------
best_model = max(accuracies, key=accuracies.get)

print("\n--- Arena Winner ---")
print(f"{best_model} with accuracy: {accuracies[best_model]}")