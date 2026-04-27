import re
import joblib
import os

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def load_models():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models")

    vectorizer = joblib.load(os.path.join(MODEL_PATH, "vectorizer.pkl"))
    nb         = joblib.load(os.path.join(MODEL_PATH, "nb.pkl"))
    lr         = joblib.load(os.path.join(MODEL_PATH, "lr.pkl"))
    svm        = joblib.load(os.path.join(MODEL_PATH, "svm.pkl"))
    scores     = joblib.load(os.path.join(MODEL_PATH, "scores.pkl"))

    return (
        vectorizer, nb, lr, svm,
        scores["f1_nb"], scores["acc_nb"],
        scores["f1_lr"], scores["acc_lr"],
        scores["f1_svm"], scores["acc_svm"]
    )

def generate_explanation(text, pred):
    text = text.lower()

    negations = ["not", "dont", "doesnt", "never", "no"]
    has_negation = any(word in text for word in negations)

    contrast_words = ["but", "however", "though", "still"]
    has_contrast = any(word in text for word in contrast_words)

    explanation = ""

    if pred == 1:
        if "check" in text or "phone" in text:
            explanation = "🚩 Bro… why is he doing phone checking like it's his side hobby?? that's sus ngl."
        elif "trust" in text and has_negation:
            explanation = "🚩 No trust?? bro that's not a small issue, that's literally the entire relationship collapsing 💀 you can't build anything solid on doubt tbh."
        elif "jealous" in text:
            explanation = "🚩 This ain't cute jealousy anymore bro… this is the draining type. Gets toxic real fast, no cap."
        elif "control" in text or "wear" in text:
            explanation = "🚩 Trying to control what you wear?? bro that's not love, that's control straight up. Giving insecure and possessive vibes… very sus."
        elif "apolog" in text:
            explanation = "🚩 Apologizing and repeating?? bro that's a loop, not growth 💀 don't fall for the same script again."
        elif "ignore" in text or "ghost" in text:
            explanation = "🚩 Ignoring or ghosting you?? lol that's not 'space', that's bad communication. Giving low effort, mid behavior."
        elif "lie" in text:
            explanation = "🚩 Lying?? bro once trust breaks, it's hard to come back. This is serious, no cap."
        elif "manipulat" in text or "gaslight" in text:
            explanation = "🚩 This is straight up manipulation bro… don't go delulu thinking it's normal. It's not."
        elif "angry" in text or "shout" in text:
            explanation = "🚩 Getting angry over small things?? yeah that's unstable behavior. You'll end up walking on eggshells."
        elif "compare" in text:
            explanation = "🚩 Comparing you to others?? nah bro that kills confidence. Not okay at all."
        elif "pressure" in text:
            explanation = "🚩 Pressuring you into things?? yeah that's crossing boundaries. Big red flag, no debate."
        elif "disrespect" in text:
            explanation = "🚩 Disrespecting you openly?? bro why are we even tolerating this 💀"
        elif "commit" in text:
            explanation = "🚩 Avoiding commitment but still acting close?? yeah that's situationship energy, don't get stuck there."
        elif "cheat" in text:
            explanation = "🚩 Broo.. BLOCK THEM RN! Cheating is not a mistake, that's a choice 💀 once loyalty is gone, everything else is just damage control."
        elif "career" in text or "job" in text or "goal" in text:
            explanation = "🚩 Undermining your career?? bro that's not support, that's insecurity. You need someone who cheers you on, not holds you back."
        elif "friend" in text:
            explanation = "🚩 Controlling your friendships?? that's isolation behavior. Major red flag — your social life is yours, not theirs to manage."
        else:
            explanation = "🚩 This is giving red flag energy bro… might seem small now but these things usually get worse, not better."

        if has_contrast:
            explanation += "\n\n⚠️ Also bro… that 'but' part? good moments don't cancel out bad patterns, no cap."
        if "apolog" in text:
            explanation += "\n\n🚩 And apologizing later doesn't fix the pattern tho! it doesn't really fix it if the behavior keeps repeating 💀"

    else:
        if "trust" in text and not has_negation:
            explanation = "✅ Trust is there?? okay bet, that's a solid foundation. Rare but we love to see it."
        elif "respect" in text or "privacy" in text:
            explanation = "✅ Respecting your space?? main character energy fr. That's how it should be."
        elif "support" in text:
            explanation = "✅ Supporting your goals?? sheesh that's a green flag no cap. Good energy."
        elif "communicat" in text:
            explanation = "✅ Good communication?? bro that alone puts this above most relationships lol."
        elif "apolog" in text and not has_negation:
            explanation = "✅ Apologizing properly and actually changing?? yeah that's maturity, not just talk."
        elif "space" in text:
            explanation = "✅ Giving space when needed?? healthy behavior fr, not clingy or controlling."
        elif "listen" in text:
            explanation = "✅ Actually listening to you?? wow bare minimum but still rare lol."
        elif "kind" in text or "understand" in text:
            explanation = "✅ Kind and understanding?? yeah that's green flag energy, no doubt."
        elif "safe" in text:
            explanation = "✅ Feeling safe around them?? that's one of the biggest green flags, no cap."
        else:
            explanation = "✅ This looks healthy ngl… no weird vibes here, all good."

        if has_contrast:
            explanation += "\n\n🟡 But yeah… there's a small 'but' there 👀 just stay aware, don't ignore patterns."

    return explanation
def load_quiz_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models")

    best_model = joblib.load(os.path.join(MODEL_PATH, "quiz_model.pkl"))
    best_name  = joblib.load(os.path.join(MODEL_PATH, "quiz_model_name.pkl"))

    all_models = {}
    for name, filename in [
        ("Logistic Regression", "quiz_logistic_regression.pkl"),
        ("SVM",                 "quiz_svm.pkl"),
        ("Random Forest",       "quiz_random_forest.pkl"),
        ("KNN",                 "quiz_knn.pkl"),
    ]:
        path = os.path.join(MODEL_PATH, filename)
        if os.path.exists(path):
            all_models[name] = joblib.load(path)

    return best_model, best_name, all_models
