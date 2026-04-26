import pickle
import re

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "..", "models", "classifier.pkl")
vectorizer_path = os.path.join(BASE_DIR, "..", "models", "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

# Clean text (same as training)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


# 🔥 UPDATED Prediction function
def rule_boost(text, score):
    text = text.lower()

    triggers = [
        "i am the best",
        "no one is better",
        "everyone is jealous",
        "i know everything",
        "only i understand",
        "no one knows better than me"
    ]

    for t in triggers:
        if t in text:
            score += 30   # 🔥 boost for overconfidence
    if "everyone" in text or "no one" in text:
        score += 10

    return min(score, 100)
def detect_personality(text):
    text = text.lower()

    if "i am the best" in text or "no one is better" in text:
        return "Narcissistic Confidence"

    elif "everyone hates me" in text or "i am useless" in text:
        return "Insecurity / Negative Bias"

    elif "maybe" in text or "i feel" in text:
        return "Self-aware / Reflective"

    elif "everyone" in text or "no one" in text:
        return "Overgeneralization"

    else:
        return "Neutral"


def predict_text(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    probabilities = model.predict_proba(vector)[0]

    # base score
    score = int(probabilities[1] * 100)

    # 🔥 APPLY RULE BOOST
    score = rule_boost(text, score)

    # 🔥 BETTER LABELING
    if score < 40:
        label = "Realistic"
    elif score < 70:
        label = "Questionable"
    else:
        label = "Delusional"
    personality=detect_personality(text)

    return label, score,personality


# 🔥 Test loop
if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your thought: ")
        
        if user_input.lower() == "exit":
            break
        
        label, score = predict_text(user_input)
        
        print(f"Prediction: {label}")
        print(f"Delusion Score: {score}/100")
        