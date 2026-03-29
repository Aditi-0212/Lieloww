from llm_generator import generate_response
from scorer import score_excuse


def choose_option(title, options):
    print(f"\nSelect {title}:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        choice = input("Enter number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Invalid choice. Try again.")


def main():
    scenario = input("\nEnter Scenario: ")

    relationship_options = ["Professional","Academic","Romantic","Friend","Family"]
    seriousness_options = ["Low", "Medium", "High"]
    tone_options = ["Casual", "Apologetic", "Formal", "Emotional"]

    relationship = choose_option("Relationship", relationship_options)
    seriousness = choose_option("Seriousness", seriousness_options)
    tone = choose_option("Tone", tone_options)

    prompt = f"""
You are generating a realistic excuse.

Scenario: {scenario}
Relationship: {relationship}
Seriousness: {seriousness}
Tone: {tone}

Generate a believable excuse in 2-3 sentences.
"""

    models = ["llama3", "mistral", "gemma:7b"]
    responses = {}
    scores = {}

    for m in models:
        print(f"\nGenerating from {m}...")
        response = generate_response(m, prompt)
        print(f"\nResponse from {m}:")
        print(response)
        responses[m] = response
        scores[m] = score_excuse(response)

    best_model = max(scores, key=scores.get)

    print("\n--- MODEL SCORES ---")
    for m in scores:
        print(f"{m}: {scores[m]:.3f}")

    print("\n--- SELECTED MODEL ---")
    print(best_model)

    print("\n--- FINAL EXCUSE ---")
    print(responses[best_model])


if __name__ == "__main__":
    main()
# from llm_generator import generate_response
# from scorer import score_excuse
# import concurrent.futures


# def choose_option(title, options):
#     print(f"\nSelect {title}:")
#     for i, option in enumerate(options, 1):
#         print(f"{i}. {option}")

#     while True:
#         choice = input("Enter number: ")
#         if choice.isdigit() and 1 <= int(choice) <= len(options):
#             return options[int(choice) - 1]
#         else:
#             print("Invalid choice. Try again.")


# def main():
#     scenario = input("\nEnter Scenario: ")

#     relationship_options = ["Friend", "Partner", "Boss", "Parent", "Colleague"]
#     seriousness_options = ["Low", "Medium", "High"]
#     tone_options = ["Casual", "Apologetic", "Professional", "Emotional", "Defensive"]

#     relationship = choose_option("Relationship", relationship_options)
#     seriousness = choose_option("Seriousness", seriousness_options)
#     tone = choose_option("Tone", tone_options)

#     prompt = f"""
# You are generating a realistic excuse.

# Scenario: {scenario}
# Relationship: {relationship}
# Seriousness: {seriousness}
# Tone: {tone}

# Generate a believable excuse in maximum 2 short sentences.
# """

#     models = ["llama3", "mistral", "gemma:2b"]

#     responses = {}
#     scores = {}

#     # 🔥 Parallel execution starts here
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future_to_model = {
#             executor.submit(generate_response, m, prompt): m
#             for m in models
#         }

#         for future in concurrent.futures.as_completed(future_to_model):
#             model_name = future_to_model[future]
#             try:
#                 response = future.result()
#                 responses[model_name] = response
#                 scores[model_name] = score_excuse(response)
#             except Exception as e:
#                 print(f"{model_name} failed: {e}")

#     best_model = max(scores, key=scores.get)

#     print("\n--- MODEL SCORES ---")
#     for m in scores:
#         print(f"{m}: {scores[m]:.3f}")

#     print("\n--- SELECTED MODEL ---")
#     print(best_model)

#     print("\n--- FINAL EXCUSE ---")
#     print(responses[best_model])


# if __name__ == "__main__":
#     main()