import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

# Path setup
DATA_PATH = "../data/believability_dataset_1200.csv"
MODEL_PATH = "../models/believability_model.pkl"
VECTORIZER_PATH = "../models/vectorizer.pkl"

# Load dataset
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Convert to binary labels
df["label"] = df["Believability_Score"].apply(lambda x: 1 if x >= 3 else 0)

X = df["Excuse_Text"]
y = df["label"]

print("Class Distribution:")
print(y.value_counts())

# Text Vectorization
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2),
    stop_words="english"
)

X_vectorized = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# Train model
model = LogisticRegression(max_iter=2000)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Save files
pickle.dump(model, open(MODEL_PATH, "wb"))
pickle.dump(vectorizer, open(VECTORIZER_PATH, "wb"))

print("Model and vectorizer saved successfully.")