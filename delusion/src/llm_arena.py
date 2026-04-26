import ollama


# 🎭 Mode-based prompt builder (UPGRADED)
# def build_prompt(user_input, mode, label, score):
    
#     base_instruction = f"""
# You are a close friend helping someone reflect on their thoughts.

# Thought: "{user_input}"
# Prediction: {label}
# Delusion Score: {score}/100

# Interpretation:
# - 0–30: Mostly realistic
# - 31–70: Uncertain / mixed
# - 71–100: Likely delusional

# Guidelines:
# - Talk like a real human, not a robot
# - Give a punchy 3-4 line reality check.
# - No bullet points
# - No formal tone
# - Keep it natural and conversational
# """

#     if mode == "savage":
#         tone = "You are brutally honest. No sugarcoating. Be blunt, slightly harsh, and directly call out irrational thinking. Like a close friend teasing you."
#     elif mode == "supportive":
#         tone = "Be kind, empathetic, and supportive."
#     elif mode == "logical":
#         tone = "Be rational, objective, analytical, and clear like a thoughtful friend."
#     else:
#         tone = "Be neutral."

#     return base_instruction + f"\nTone: {tone}\n\nFormat:\nAnalysis:\n- point 1\n- point 2\n- point 3\n\nConclusion:\n..."
def build_prompt(user_input, mode, label, score):
    
    if mode == "savage":
        tone = "You are brutally honest. No sugarcoating. Be blunt, slightly harsh, and directly call out irrational thinking. Like a close friend teasing you."
    elif mode == "supportive":
        tone = "Be warm, kind and empathetic like a caring friend."
    elif mode == "logical":
        tone = "Be rational and analytical but still conversational."
    else:
        tone = "Be neutral."

    return f"""
You are a close friend giving a quick reality check.

Thought: "{user_input}"
Delusion Score: {score}/100 (0=realistic, 100=delusional)
Prediction: {label}

{tone}

Your job:
- Talk like a real friend (natural, flowing)
- Explain clearly but not like a robot
- Be slightly blunt but caring
- CALL OUT delusion clearly.

Rules:
- Be direct, sharp, and slightly harsh
- Do NOT comfort or sugarcoat
- Point out flaws in thinking immediately
- Use a confident, slightly sarcastic tone
- No long explanations
- No bullet points
- Max 80–120 words

Talk like a smart friend who is done tolerating nonsense.
"""

# Give a punchy 3-4 line reality check.

# ⚡ LLM response (with control)
def get_llm_response(model_name, prompt):
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options = {
                "temperature": 0.85,
                "num_predict": 250,
                "top_k": 40,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_ctx": 1024,
            }
        )
        return response['message']['content']

    except Exception as e:
        return f"Error from {model_name}: {str(e)}"


# 🧠 Arena runner (UPDATED)
def run_arena(user_input, mode, label, score):
    
    models = ["llama3"]   # 🔥 switched from llama3 → mistral

    responses = {}

    # Build prompt
    prompt = build_prompt(user_input, mode, label, score)

    for model in models:
        print(f"\nGenerating from {model} ({mode} mode)...")
        reply = get_llm_response(model, prompt)
        responses[model] = reply

    return responses


# 🔥 MAIN TEST
if __name__ == "__main__":
    
    user_input = input("Enter your thought: ")
    mode = input("Choose mode (savage/supportive/logical): ").lower()

    # ⚠️ TEMP MOCK (replace with your ML model later)
    from predict import predict_text
    label, score = predict_text(user_input)
    outputs = run_arena(user_input, mode, label, score)

    for model, response in outputs.items():
        print(f"\n--- {model.upper()} ({mode}) ---")
        print(response)

