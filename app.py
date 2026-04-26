# import streamlit as st
# import pandas as pd
# import time

# from excuse_generator.src.llm_generator import generate_response
# from excuse_generator.src.scorer import score_excuse
# from delusion.src.llm_arena import run_arena
# from delusion.src.predict import predict_text
# from red_flag.redflag_utils import clean_text, generate_explanation, load_models

# # -------------------------------------------------
# # PAGE CONFIG
# # -------------------------------------------------

# st.set_page_config(
#     page_title="LieLow ⚡",
#     page_icon="⚡",
#     layout="wide"
# )


# # -------------------------------------------------
# # STYLING
# # -------------------------------------------------

# st.markdown("""
# <style>

# body {
#     background-color: #0f172a;
# }

# .hero {
#     text-align:center;
#     padding-top:20px;
# }

# .hero h1 {
#     font-size:3rem;
#     color:#38bdf8;
# }

# .hero p {
#     color:#cbd5e1;
#     font-size:1.2rem;
# }

# .module-card {
#     background:#1e293b;
#     padding:25px;
#     border-radius:15px;
#     text-align:center;
#     box-shadow:0px 8px 25px rgba(0,0,0,0.4);
#     transition:0.25s;
# }

# .module-card:hover {
#     transform:scale(1.05);
# }

# .stButton button {
#     background:#38bdf8;
#     color:black;
#     font-weight:bold;
#     border-radius:10px;
#     height:45px;
# }

# </style>
# """, unsafe_allow_html=True)
# st.markdown("### Choose your chaos today 😌")


# # -------------------------------------------------
# # SESSION STATE
# # -------------------------------------------------

# if "page" not in st.session_state:
#     st.session_state.page = "home"

# def go_home():
#     st.session_state.page = "home"

# def open_excuse_hub():
#     st.session_state.page = "excuse_hub"

# def open_excuse_gen():
#     st.session_state.page = "excuse_gen"

# def open_believability():
#     st.session_state.page = "believability"

# def open_redflag():
#     st.session_state.page = "redflag"

# def open_situationship():
#     st.session_state.page = "situationship"

# def open_delusion():
#     st.session_state.page="delusion"


# # =================================================
# # HOME PAGE
# # =================================================

# if st.session_state.page == "home":

#     st.markdown("""
#     <div class="hero">
#         <h1>⚡ LieLow : AI Life Toolkit</h1>
#         <p>Smart AI tools for chaotic Gen-Z lives</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.write("")
#     st.write("")

#     col1, col2 = st.columns(2)
#     col3, col4 = st.columns(2)

#     with col1:

#         st.markdown("""
#         <div class="module-card">
#         <h3>🤖 Excuse Generator</h3>
#         <p>Generate believable excuses using multiple AI models.</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Open Excuse Generator", use_container_width=True):
#             open_excuse_hub()

#     with col2:

#         st.markdown("""
#         <div class="module-card">
#         <h3>💭 Am I Delusional?</h3>
#         <p>AI powered reality check.</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Open Module", use_container_width=True):
#             open_delusion()

#     with col3:

#         st.markdown("""
#         <div class="module-card">
#         <h3>🚩 Red Flag Checker</h3>
#         <p>Analyze chats for toxic patterns.</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Open Module ", use_container_width=True):
#             open_redflag()

#     with col4:

#         st.markdown("""
#         <div class="module-card">
#         <h3>💔 Situationship Survival</h3>
#         <p>AI advice for confusing relationships.</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Open Module  ", use_container_width=True):
#             open_situationship()



# # =================================================
# # WORK IN PROGRESS PAGE
# # =================================================

# # elif st.session_state.page == "wip":

# #     st.button("⬅ Back to Home", on_click=go_home)

# #     st.markdown("## 🚧 Module Under Development")

# #     st.info("We're building something cool here. Stay tuned.")

# #===============================
# #EXCUSEHUB
# #===============================

# elif st.session_state.page == "excuse_hub":

#     st.button("⬅ Back", on_click=go_home)

#     st.title("🤖 Excuse Engine")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("""
#         <div class="module-card">
#         <h3>🎭 Generate Excuse</h3>
#         <p>Create smart AI excuses</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Generate Excuse", use_container_width=True):
#             open_excuse_gen()

#     with col2:
#         st.markdown("""
#         <div class="module-card">
#         <h3>📊 Believability Checker</h3>
#         <p>Evaluate how convincing your excuse is</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Check Believability", use_container_width=True):
#             open_believability()

# # =================================================
# # EXCUSE GENERATOR PAGE
# # =================================================

# elif st.session_state.page == "excuse_gen":

#     st.button("⬅ Back to Home", on_click=go_home)

#     st.title("🤖 AI Excuse Generator")

#     st.write("Generate **believable excuses using multiple LLM models**")

#     st.write("---")

#     # INPUT SECTION

#     col1, col2 = st.columns(2)

#     with col1:

#         scenario = st.text_input("📌 Enter your situation")

#         relationship = st.selectbox(
#             "👥 Relationship Type",
#             ["Professional", "Academic", "Romantic", "Friend", "Family"]
#         )

#     with col2:

#         seriousness = st.selectbox(
#             "⚠ Seriousness Level",
#             ["Low", "Medium", "High"]
#         )

#         tone = st.selectbox(
#             "🎭 Tone",
#             ["Casual", "Apologetic", "Formal", "Emotional"]
#         )

#     st.write("")

#     # GENERATE BUTTON

#     if st.button("⚡ Generate Excuse", use_container_width=True):

#         prompt = f"""
#         You are generating a realistic excuse.

#         Scenario: {scenario}
#         Relationship: {relationship}
#         Seriousness: {seriousness}
#         Tone: {tone}

#         Generate a believable excuse in 2 sentences.
#         """

#         models = ["llama3", "mistral", "gemma:7b"]

#         responses = {}
#         scores = {}

#         st.write("---")
#         st.subheader("⚔️ LLM Model Arena")

#         progress = st.progress(0)

#         for i, m in enumerate(models):

#             st.info(f"🧠 {m} is thinking...")

#             response = generate_response(m, prompt)
#             score = float(score_excuse(response))

#             responses[m] = response
#             scores[m] = score

#             st.write(f"### 🤖 {m}")

#             col1, col2 = st.columns([3,1])

#             with col1:
#                 st.success(response)

#             with col2:
#                 st.metric("Believability", f"{score:.3f}")

#             st.write("---")

#             progress.progress((i+1)/len(models))


#         # LEADERBOARD

#         st.subheader("📊 Arena Leaderboard")

#         data = {
#             "Model": list(scores.keys()),
#             "Believability Score": list(scores.values())
#         }

#         df = pd.DataFrame(data)
#         df = df.sort_values(by="Believability Score", ascending=False)

#         st.dataframe(df, use_container_width=True)


#         # WINNER REVEAL ANIMATION

#         st.write("---")
#         st.subheader("⚔️ Determining Arena Winner...")

#         with st.spinner("Evaluating models..."):
#             time.sleep(2)

#         winner = max(scores, key=scores.get)
#         st.toast(f"🏆 {winner} dominated the arena!")
#         progress_bar = st.progress(0)

#         for i in range(100):
#             time.sleep(0.01)
#             progress_bar.progress(i + 1)

#         st.write("")
#         st.markdown(
# """
# <h1 style='text-align:center; color:#38bdf8'>
# 🏆 ARENA CHAMPION 🏆
# </h1>
# """,
# unsafe_allow_html=True
# )

#         st.balloons()

#         winner_col1, winner_col2 = st.columns([3,1])

#         with winner_col1:
#             st.success(responses[winner])

#         with winner_col2:
#             st.metric("Winning Model", winner)
#             st.metric("Believability Score", f"{scores[winner]:.3f}")

# #================================================
# #belivabilty
# #================================================

# elif st.session_state.page == "believability":

#     st.button("⬅ Back", on_click=open_excuse_hub)

#     st.title("📊 Believability Checker")

#     user_excuse = st.text_area("Enter your excuse")

#     if st.button("Analyze", use_container_width=True):

#         if user_excuse.strip() == "":
#             st.warning("Enter an excuse first")
#             st.stop()

#         score = float(score_excuse(user_excuse))

#         st.metric("Believability Score", f"{score:.3f}")

#         if score > 0.7:
#             st.success("🔥 Highly believable")
#         elif score > 0.4:
#             st.warning("⚠️ Medium believable")
#         else:
#             st.error("❌ Sounds fake bro")

# # =================================================
# # DELUSION PAGE
# # =================================================

# elif st.session_state.page == "delusion":

#     st.button("⬅ Back to Home", on_click=go_home)

#     #----------------
#     # AM I DELUSIONAL
#     #--------------------
#     if "is_analyzing" not in st.session_state:
#         st.session_state.is_analyzing = False
#     if "mode" not in st.session_state:
#         st.session_state.mode = None

#     st.title("🧠 Am I Delusional?")

#     if st.session_state.mode is None:
#         st.subheader("Choose your mode")

#         col1, col2, col3 = st.columns(3)

#         if col1.button("🔥 Savage"):
#             st.session_state.mode = "savage"

#         if col2.button("💙 Supportive"):
#             st.session_state.mode = "supportive"

#         if col3.button("⚙️ Logical"):
#             st.session_state.mode = "logical"

#         st.stop()

#     mode = st.session_state.mode
    
#     def set_mode_style(mode):

#         if mode == "savage":
#             bg = "linear-gradient(135deg, #1f0000, #7f1d1d)"
#             text = "#ff4d4d"

#         elif mode == "supportive":
#             bg = "linear-gradient(135deg, #2e1065, #9333ea)"
#             text = "#c4b5fd"

#         elif mode == "logical":
#             bg = "linear-gradient(135deg, #0f172a, #1e3a8a)"
#             text = "#93c5fd"

#         st.markdown(f"""
#     <style>
#     .stApp {{
#         background: {bg};
#         color: white;
#     }}
    

#     .mode-title {{
#         text-align:center;
#         font-size:2rem;
#         font-weight:bold;
#         color:{text};
#         margin-bottom:20px;
#     }}

#     .glass {{
#         background: rgba(255,255,255,0.08);
#         padding:20px;
#         border-radius:15px;
#         backdrop-filter: blur(10px);
#         box-shadow:0px 8px 30px rgba(0,0,0,0.4);
#     }}
#     .stButton button {{
#     background: linear-gradient(135deg, #38bdf8, #0ea5e9);
#     color: black;
#     font-weight: bold;
#     border-radius: 12px;
#     height: 50px;
#     transition: 0.3s;
#     box-shadow: 0px 0px 15px rgba(56,189,248,0.5);
# }}

# .stButton button:hover {{
#     transform: scale(1.05);
#     box-shadow: 0px 0px 25px rgba(56,189,248,0.9);
# }}

# .pulse {{
#     animation: pulse 1.5s infinite;
# }}

# @keyframes pulse {{
#     0% {{ box-shadow: 0 0 0 0 rgba(56,189,248, 0.7); }}
#     70% {{ box-shadow: 0 0 0 20px rgba(56,189,248, 0); }}
#     100% {{ box-shadow: 0 0 0 0 rgba(56,189,248, 0); }}
# }}



#     </style>
#     """, unsafe_allow_html=True)


#     if mode == "savage":
#         st.caption("No sugarcoating. Just truth.")
#         st.markdown("<h3 style='color:red;'>Savage Mode Activated</h3>", unsafe_allow_html=True)

#     elif mode == "supportive":
#         st.caption("Gentle clarity. You're safe here.")
#         st.markdown("<h3 style='color:blue;'>Supportive Mode Activated</h3>", unsafe_allow_html=True)

#     elif mode == "logical":
#         st.caption("Pure reasoning. No emotions involved.")
#         st.markdown("<h3 style='color:gray;'>Logical Mode Activated</h3>", unsafe_allow_html=True)

#     set_mode_style(mode)
#     st.write(f"### Mode: {mode.capitalize()}")

#     st.markdown("<div class='glass'>", unsafe_allow_html=True)

#     user_input = st.text_area("🧠 What's on your mind?", height=120)

#     button_text = "⏳ Analyzing..." if st.session_state.is_analyzing else "⚡ Analyze Reality"

#     analyze_clicked = st.button(
#     button_text,
#     use_container_width=True,
#     disabled=st.session_state.is_analyzing,
#     key="analyze_btn"
# )

#     st.markdown("</div>", unsafe_allow_html=True)

#     if analyze_clicked:
#         st.session_state.is_analyzing = True
#         with st.spinner("🧠 Breaking down your thoughts..."):
#             time.sleep(1)

#         st.info("⚡ Running psychological analysis...")
#         time.sleep(1)

#         if user_input.strip() == "":
#             st.warning("Please enter a thought first.")
#             st.session_state.is_analyzing = False
#             st.stop()

#         with st.spinner("🧠 Thinking... this might take a few seconds..."):

#             label, score,personality = predict_text(user_input)
#             responses = run_arena(user_input, mode, label, score)
#         st.subheader(f"personality:{personality}")
#         st.subheader(f"Prediction: {label}")
#         st.write(f"Delusion Score: {score}/100")
#         st.progress(score / 100)

#         for model, response in responses.items():
#             with st.container():
#                 st.markdown(f"### 🤖 {model.upper()}")
#                 placeholder = st.empty()

#                 text = ""
#                 for char in response:
#                     text += char
#                     placeholder.markdown(f"<div class='glass'>{text}</div>", unsafe_allow_html=True)
#                     time.sleep(0.01)

#     # ✅ RE-ENABLE BUTTON AFTER DONE
#         st.session_state.is_analyzing = False

#     if st.button("Change Mode",key="change_mode_btn"):
#         st.session_state.mode = None
#         st.rerun()

# #==============================================
# #RED FLAG
# #==============================================

# elif st.session_state.page == "redflag":

#     st.button("⬅ Back to Home", on_click=go_home)  # ← fix this too
#     st.title("🚩 Red Flag Detector")

#     # ---- TAB LAYOUT ----
#     tab1, tab2 = st.tabs(["💬 Scenario Analyzer", "📋 Relationship Quiz"])

#     # ================================================
#     # TAB 1 — SCENARIO ANALYZER (your model arena)
#     # ================================================
#     with tab1:
#         st.subheader("Describe what's going on")
#         st.caption("Type any situation and the AI models will analyze it")

#         user_input = st.text_area(
#             "📝 What happened?",
#             placeholder="e.g. He checks my phone every night and gets angry when I talk to my friends...",
#             height=120
#         )

#         if st.button("⚡ Analyze", use_container_width=True, key="analyze_scenario"):

#             if user_input.strip() == "":
#                 st.warning("Type something first 💀")
#                 st.stop()

#             clean = clean_text(user_input)
#             vec = vectorizer.transform([clean])

#             results = {}

#             prob_nb = max(nb.predict_proba(vec)[0])
#             pred_nb = nb.predict(vec)[0]
#             results['Naive Bayes'] = (f1_nb, acc_nb, pred_nb, prob_nb)

#             prob_lr = max(lr.predict_proba(vec)[0])
#             pred_lr = lr.predict(vec)[0]
#             results['Logistic Regression'] = (f1_lr, acc_lr, pred_lr, prob_lr)

#             prob_svm = max(svm.predict_proba(vec)[0])
#             pred_svm = svm.predict(vec)[0]
#             results['SVM'] = (f1_svm, acc_svm, pred_svm, prob_svm)

#             inputs = tokenizer(clean, return_tensors="pt", truncation=True, padding=True, max_length=128)
#             outputs = model(**inputs)
#             probs = torch.softmax(outputs.logits, dim=1)
#             bert_pred = torch.argmax(probs, dim=1).item()
#             bert_conf = torch.max(probs).item()
#             results['DistilBERT'] = (0.90, None, bert_pred, bert_conf)

#             # Arena display
#             st.write("---")
#             st.subheader("⚔️ Model Arena")

#             for name, (f1, acc, pred, prob) in results.items():
#                 col1, col2 = st.columns([3, 1])
#                 with col1:
#                     label = "🚩 Red Flag" if pred == 1 else "✅ Green Flag"
#                     st.info(f"{name}: {label}")
#                 with col2:
#                     st.metric("Confidence", f"{prob:.2f}")

#             # Best model verdict
#             best_model = max(results, key=lambda x: results[x][0])
#             _, _, best_pred, best_conf = results[best_model]

#             strong_red_flags = ["cheat", "abuse", "hit", "violence"]
#             if any(word in user_input.lower() for word in strong_red_flags):
#                 best_pred = 1

#             st.write("---")
#             st.subheader("🏆 Final Verdict")

#             if best_pred == 1:
#                 st.error("🚩 RED FLAG DETECTED")
#                 st.toast("Bro… run 💀")
#             else:
#                 st.success("✅ GREEN FLAG")
#                 st.balloons()
#                 st.toast("Green flag energy 🌳")

#             st.metric("Confidence", f"{best_conf:.2f}")
#             st.write(f"Best Model: **{best_model}**")

#             # Explanation
#             explanation = generate_explanation(user_input, best_pred)
#             st.write("---")
#             st.subheader("💬 Reality Check")
#             st.markdown(f"""
#             <div style='background:rgba(255,255,255,0.08);padding:20px;border-radius:15px;backdrop-filter:blur(10px);'>
#             {explanation}
#             </div>
#             """, unsafe_allow_html=True)

#             st.write("---")
#             st.subheader("📊 Toxicity Level")
#             score = int(best_conf * 100)
#             st.progress(score / 100)
#             st.write(f"Intensity Score: {score}/100")

#     # ================================================
#     # TAB 2 — QUIZ
#     # ================================================
#     with tab2:
#         st.subheader("Quick Relationship Health Check")
#         st.caption("Answer honestly 👀")

#         questions = {
#             "avoid_label":    "Do they avoid labeling the relationship?",
#             "cancels":        "Do they cancel plans often?",
#             "mixed_signals":  "Do they give mixed signals?",
#             "low_effort":     "Do they put in low effort?",
#             "avoids_future":  "Do they avoid talking about the future?",
#             "jealous":        "Are they excessively jealous or controlling?",
#             "phone_check":    "Do they check your phone or monitor you?",
#             "gaslights":      "Do they make you question your own feelings?",
#         }

#         answers = {}
#         for key, q in questions.items():
#             answers[key] = st.radio(q, ["No", "Yes"], horizontal=True, key=key)

#         if st.button("🔍 Get My Result", use_container_width=True, key="quiz_submit"):

#             score = sum(1 for v in answers.values() if v == "Yes")
#             total = len(questions)
#             pct = int((score / total) * 100)

#             st.write("---")
#             st.subheader("📊 Your Score")
#             st.progress(pct / 100)
#             st.write(f"**{score}/{total} red flags detected**")

#             if score == 0:
#                 st.success("✅ Zero red flags. This actually sounds healthy?? rare.")
#             elif score <= 2:
#                 st.warning("🟡 A couple yellow flags. Worth keeping an eye on.")
#             elif score <= 5:
#                 st.error("🚩 Multiple red flags. This is giving toxic era.")
#             else:
#                 st.error("🆘 Major red flags detected. Bro please talk to someone you trust.")
#                 st.toast("This ain't it 💀")

#             # Personalized message based on worst answers
#             flagged = [q for k, q in questions.items() if answers[k] == "Yes"]
#             if flagged:
#                 st.write("---")
#                 st.subheader("💬 What stood out")
#                 for f in flagged:
#                     st.markdown(f"- 🚩 {f}")

# #=================================================
# #SITUATIONSHIP
# #==================================================
# elif st.session_state.page == "situationship":

#     st.button("⬅ Back", on_click=open_situationship)

#     st.title("💔 Situationship Survival")

#     questions = {
#         "avoid_label": "Avoid labeling relationship?",
#         "cancels": "Cancels plans often?",
#         "mixed_signals": "Gives mixed signals?",
#         "effort": "Low effort?",
#         "future": "Avoids future talk?"
#     }

#     answers = {}

#     for key, q in questions.items():
#         answers[key] = st.selectbox(q, ["No", "Yes"])

#     if st.button("Analyze"):

#         score = sum([1 if v=="Yes" else 0 for v in answers.values()])

#         st.metric("Toxic Score", score)

#         if score >= 3:
#             st.error("💔 This ain't it.")
#         else:
#             st.success("💚 Has potential")