import streamlit as st
import pandas as pd
import time

from src.llm_generator import generate_response
from src.scorer import score_excuse


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="LieLow ⚡",
    page_icon="⚡",
    layout="wide"
)


# -------------------------------------------------
# STYLING
# -------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.hero {
    text-align:center;
    padding-top:20px;
}

.hero h1 {
    font-size:3rem;
    color:#38bdf8;
}

.hero p {
    color:#cbd5e1;
    font-size:1.2rem;
}

.module-card {
    background:#1e293b;
    padding:25px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 8px 25px rgba(0,0,0,0.4);
    transition:0.25s;
}

.module-card:hover {
    transform:scale(1.05);
}

.stButton button {
    background:#38bdf8;
    color:black;
    font-weight:bold;
    border-radius:10px;
    height:45px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

def open_excuse():
    st.session_state.page = "excuse"

def open_wip():
    st.session_state.page = "wip"


# =================================================
# HOME PAGE
# =================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <h1>⚡ LieLow : AI Life Toolkit</h1>
        <p>Smart AI tools for chaotic Gen-Z lives</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="module-card">
        <h3>🤖 Excuse Generator</h3>
        <p>Generate believable excuses using multiple AI models.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Excuse Generator", use_container_width=True):
            open_excuse()

    with col2:

        st.markdown("""
        <div class="module-card">
        <h3>💭 Am I Delusional?</h3>
        <p>AI powered reality check.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Module", use_container_width=True):
            open_wip()

    with col3:

        st.markdown("""
        <div class="module-card">
        <h3>🚩 Red Flag Checker</h3>
        <p>Analyze chats for toxic patterns.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Module ", use_container_width=True):
            open_wip()

    with col4:

        st.markdown("""
        <div class="module-card">
        <h3>💔 Situationship Survival</h3>
        <p>AI advice for confusing relationships.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Module  ", use_container_width=True):
            open_wip()



# =================================================
# WORK IN PROGRESS PAGE
# =================================================

elif st.session_state.page == "wip":

    st.button("⬅ Back to Home", on_click=go_home)

    st.markdown("## 🚧 Module Under Development")

    st.info("We're building something cool here. Stay tuned.")



# =================================================
# EXCUSE GENERATOR PAGE
# =================================================

elif st.session_state.page == "excuse":

    st.button("⬅ Back to Home", on_click=go_home)

    st.title("🤖 AI Excuse Generator")

    st.write("Generate **believable excuses using multiple LLM models**")

    st.write("---")

    # INPUT SECTION

    col1, col2 = st.columns(2)

    with col1:

        scenario = st.text_input("📌 Enter your situation")

        relationship = st.selectbox(
            "👥 Relationship Type",
            ["Professional", "Academic", "Romantic", "Friend", "Family"]
        )

    with col2:

        seriousness = st.selectbox(
            "⚠ Seriousness Level",
            ["Low", "Medium", "High"]
        )

        tone = st.selectbox(
            "🎭 Tone",
            ["Casual", "Apologetic", "Formal", "Emotional"]
        )

    st.write("")

    # GENERATE BUTTON

    if st.button("⚡ Generate Excuse", use_container_width=True):

        prompt = f"""
        You are generating a realistic excuse.

        Scenario: {scenario}
        Relationship: {relationship}
        Seriousness: {seriousness}
        Tone: {tone}

        Generate a believable excuse in 2 sentences.
        """

        models = ["llama3", "mistral", "gemma:7b"]

        responses = {}
        scores = {}

        st.write("---")
        st.subheader("⚔️ LLM Model Arena")

        progress = st.progress(0)

        for i, m in enumerate(models):

            st.info(f"🧠 {m} is thinking...")

            response = generate_response(m, prompt)
            score = float(score_excuse(response))

            responses[m] = response
            scores[m] = score

            st.write(f"### 🤖 {m}")

            col1, col2 = st.columns([3,1])

            with col1:
                st.success(response)

            with col2:
                st.metric("Believability", f"{score:.3f}")

            st.write("---")

            progress.progress((i+1)/len(models))


        # LEADERBOARD

        st.subheader("📊 Arena Leaderboard")

        data = {
            "Model": list(scores.keys()),
            "Believability Score": list(scores.values())
        }

        df = pd.DataFrame(data)
        df = df.sort_values(by="Believability Score", ascending=False)

        st.dataframe(df, use_container_width=True)


        # WINNER REVEAL ANIMATION

        st.write("---")
        st.subheader("⚔️ Determining Arena Winner...")

        with st.spinner("Evaluating models..."):
            time.sleep(2)

        winner = max(scores, key=scores.get)
        st.toast(f"🏆 {winner} dominated the arena!")
        progress_bar = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
        progress_bar.progress(i + 1)

        st.write("")
        st.markdown(
"""
<h1 style='text-align:center; color:#38bdf8'>
🏆 ARENA CHAMPION 🏆
</h1>
""",
unsafe_allow_html=True
)

        st.balloons()

        winner_col1, winner_col2 = st.columns([3,1])

        with winner_col1:
            st.success(responses[winner])

        with winner_col2:
            st.metric("Winning Model", winner)
            st.metric("Believability Score", f"{scores[winner]:.3f}")