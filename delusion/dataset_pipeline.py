import ollama
import json
import pandas as pd
from tqdm import tqdm
import time

MODELS = ["llama3", "mistral", "gemma"]

# -------------------------
# 1. DATA GENERATION FUNCTION
# -------------------------
def generate_from_model(model_name):
    PROMPT = """
Generate 5 realistic human thoughts.

Each thought must include:
- text
- label (Realistic or Delusional)
- category

Return ONLY valid JSON list.
"""

    try:
        print(f"Generating from {model_name}...")

        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": PROMPT}]
        )

        content = response['message']['content']

        # Extract JSON safely
        start = content.find('[')
        end = content.rfind(']') + 1
        json_str = content[start:end]

        data = json.loads(json_str)
        return data

    except Exception as e:
        print(f"Error in {model_name}: {e}")
        return []


# -------------------------
# 2. DATASET CREATION
# -------------------------
def generate_dataset(iterations=5):
    data = []

    for i in tqdm(range(iterations)):
        print(f"\nIteration {i+1}")

        for model in MODELS:
            results = generate_from_model(model)

            for item in results:
                item["source_model"] = model
                data.append(item)

        time.sleep(1)  # prevent overload

    return data


# -------------------------
# 3. CONSENSUS FUNCTION (LIMITED USE)
# -------------------------
def consensus_label(row):
    votes = []

    for model in MODELS:
        prompt = f"""
Classify the thought STRICTLY as:
Realistic or Delusional

Return ONLY JSON:
{{
  "label": "...",
  "confidence": 0-1
}}

Thought: "{row['text']}"
"""
        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response['message']['content']
            json_str = content[content.find('{'):content.rfind('}')+1]
            result = json.loads(json_str)

            votes.append(result["label"])

        except:
            continue

    if votes:
        return max(set(votes), key=votes.count)
    return None


# -------------------------
# 4. MAIN EXECUTION
# -------------------------
if __name__ == "__main__":
    print("🚀 Generating dataset...")

    dataset = generate_dataset(iterations=5)

    df = pd.DataFrame(dataset)

    # Remove duplicates
    df = df.drop_duplicates(subset=["text"])

    print(f"Dataset size: {len(df)}")

    # ✅ SAVE RAW DATA FIRST (VERY IMPORTANT)
    df.to_csv("raw_dataset.csv", index=False, encoding="utf-8-sig")
    print("✅ Raw dataset saved as raw_dataset.csv")

    # -------------------------
    # ⚡ FAST MODE (RECOMMENDED)
    # -------------------------
    df["final_label"] = df["label"]

    # -------------------------
    # 🔥 OPTIONAL: LIMITED CONSENSUS (only 20 rows)
    # -------------------------
    print("Applying consensus on small sample...")

    sample_df = df.sample(min(20, len(df)))

    sample_df["final_label"] = sample_df.apply(consensus_label, axis=1)

    # Replace labels in main dataframe
    df.update(sample_df)

    # -------------------------
    # FINAL SAVE
    # -------------------------
    df.to_csv("final_dataset.csv", index=False, encoding="utf-8-sig")

    print("🎉 DONE! Final dataset saved as final_dataset.csv")