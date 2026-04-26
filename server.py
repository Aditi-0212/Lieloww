from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor
from groq import Groq
import os

from excuse_generator.src.scorer import score_excuse
from delusion.src.predict import predict_text
from red_flag.redflag_utils import clean_text, generate_explanation, load_models

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- Groq client (put your key in an env var, don't hardcode it) ---
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

executor = ThreadPoolExecutor(max_workers=6)

# Load sklearn models once at startup
vectorizer, nb, lr, svm, f1_nb, acc_nb, f1_lr, acc_lr, f1_svm, acc_svm = load_models()
print("Server started")

# Groq model names (fast, free)
GROQ_MODELS = {
    "Llama 3":  "llama-3.3-70b-versatile",
    "Mistral":  "llama-3.1-8b-instant",
    "Gemma 7B": "meta-llama/llama-4-scout-17b-16e-instruct",
}

def groq_chat(model_id: str, prompt: str) -> str:
    """Single blocking Groq call — runs in thread pool."""
    completion = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.8,
    )
    return completion.choices[0].message.content.strip()


# ── EXCUSE ──────────────────────────────────────────────────────────────────

class ExcuseRequest(BaseModel):
    scenario: str
    relationship: str
    seriousness: str
    tone: str

def _run_one_excuse(name: str, model_id: str, prompt: str):
    response = groq_chat(model_id, prompt)
    score = float(score_excuse(response))
    return name, {"response": response, "score": score}

@app.post("/generate-excuse")
async def generate_excuse(req: ExcuseRequest):
    prompt = (
        f"Generate a believable excuse in exactly 2 sentences.\n"
        f"Scenario: {req.scenario}\n"
        f"Relationship: {req.relationship}\n"
        f"Seriousness: {req.seriousness}\n"
        f"Tone: {req.tone}\n"
        f"Reply with only the excuse, nothing else."
    )
    loop = asyncio.get_event_loop()
    # All 3 models fire in PARALLEL — total wait = slowest single call (~1-2s on Groq)
    tasks = [
        loop.run_in_executor(executor, _run_one_excuse, name, model_id, prompt)
        for name, model_id in GROQ_MODELS.items()
    ]
    results_list = await asyncio.gather(*tasks)
    return dict(results_list)


# ── BELIEVABILITY ────────────────────────────────────────────────────────────

class BelievabilityRequest(BaseModel):
    excuse: str

@app.post("/check-believability")
async def check_believability(req: BelievabilityRequest):
    loop = asyncio.get_event_loop()
    score = await loop.run_in_executor(executor, score_excuse, req.excuse)
    return {"score": float(score)}


# ── DELUSION ─────────────────────────────────────────────────────────────────

class DelusionRequest(BaseModel):
    text: str
    mode: str

MODE_PROMPTS = {
    "savage":     "You are brutally honest with zero sugarcoating. Be savage but insightful.",
    "supportive": "You are warm, empathetic and supportive. Be gentle but clear.",
    "logical":    "You are purely logical. Analyze like a data scientist with no emotion.",
}

def _run_one_delusion(name: str, model_id: str, text: str, mode: str, label: str, score: int):
    system = MODE_PROMPTS.get(mode, MODE_PROMPTS["logical"])
    prompt = (
        f"Someone said: \"{text}\"\n"
        f"Our analysis: {label} (delusion score: {score}/100).\n"
        f"Give a 2-3 sentence reality check in your style. Be direct."
    )
    full_prompt = f"{system}\n\n{prompt}"
    return name, groq_chat(model_id, full_prompt)

def _run_one_delusion(name: str, model_id: str, text: str, mode: str, label: str, score: int):
    system = MODE_PROMPTS.get(mode, MODE_PROMPTS["logical"])
    prompt = (
        f"Someone said: \"{text}\"\n"
        f"Analysis: {label} (delusion score: {score}/100).\n"
        f"Give a 2-3 sentence reality check in your style. Be direct and stay in character."
    )
    return name, groq_chat(model_id, f"{system}\n\n{prompt}")

def _run_delusion(text: str, mode: str):
    label, score, personality = predict_text(text)
    # Run all 3 models in parallel
    with ThreadPoolExecutor(max_workers=3) as inner:
        futures = {
            name: inner.submit(_run_one_delusion, name, model_id, text, mode, label, score)
            for name, model_id in GROQ_MODELS.items()
        }
        responses = {name: f.result()[1] for name, f in futures.items()}
    return label, score, personality, responses

@app.post("/analyze-delusion")
async def analyze_delusion(req: DelusionRequest):
    loop = asyncio.get_event_loop()
    label, score, personality, responses = await loop.run_in_executor(
        executor, _run_delusion, req.text, req.mode
    )
    return {"label": label, "score": score, "personality": personality, "responses": responses}


# ── RED FLAG ─────────────────────────────────────────────────────────────────

class RedFlagRequest(BaseModel):
    text: str

def _run_redflag(text: str):
    clean = clean_text(text)
    vec = vectorizer.transform([clean])

    prob_nb  = float(max(nb.predict_proba(vec)[0]));  pred_nb  = int(nb.predict(vec)[0])
    prob_lr  = float(max(lr.predict_proba(vec)[0]));  pred_lr  = int(lr.predict(vec)[0])
    prob_svm = float(max(svm.predict_proba(vec)[0])); pred_svm = int(svm.predict(vec)[0])

    best_pred = pred_nb
    best_conf = prob_nb

    if any(w in text.lower() for w in ["cheat", "abuse", "hit", "violence"]):
        best_pred = 1

    explanation = generate_explanation(text, best_pred)
    return pred_nb, prob_nb, pred_lr, prob_lr, pred_svm, prob_svm, best_pred, best_conf, explanation

@app.post("/analyze-redflag")
async def analyze_redflag(req: RedFlagRequest):
    loop = asyncio.get_event_loop()
    (pred_nb, prob_nb, pred_lr, prob_lr,
     pred_svm, prob_svm, best_pred, best_conf, explanation) = await loop.run_in_executor(
        executor, _run_redflag, req.text
    )
    return {
        "models": {
            "Naive Bayes":        {"pred": pred_nb,  "conf": prob_nb},
            "Logistic Regression":{"pred": pred_lr,  "conf": prob_lr},
            "SVM":                {"pred": pred_svm, "conf": prob_svm},
        },
        "best_pred": best_pred,
        "best_conf": best_conf,
        "best_model": "Naive Bayes",
        "explanation": explanation
    }

# uvicorn server:app --reload --port 8000


# ── FEATURE 4: CHAT WITH YOUR EXCUSE ────────────────────────────────────────

class ChatExcuseRequest(BaseModel):
    messages: list  # [{role, content}]

def _chat_excuse(messages: list) -> str:
    system = "You are a witty excuse-refinement assistant. The user will ask you to modify an excuse — make it shorter, more dramatic, funnier, more formal, etc. Reply with ONLY the refined excuse, nothing else. Keep it under 3 sentences."
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages,
        max_tokens=200,
        temperature=0.9,
    )
    return completion.choices[0].message.content.strip()

@app.post("/chat-excuse")
async def chat_excuse(req: ChatExcuseRequest):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(executor, _chat_excuse, req.messages)
    return {"response": response}


# ── FEATURE 1: CHAT WITH DELUSION (conversation memory) ─────────────────────

class ChatDelusionRequest(BaseModel):
    messages: list  # full history [{role, content}]
    mode: str

def _chat_delusion(messages: list, mode: str) -> tuple:
    system = MODE_PROMPTS.get(mode, MODE_PROMPTS["logical"]) + \
        " You are continuing an ongoing conversation. Stay in character. Be concise (2-3 sentences max)."
    model_id = "llama-3.3-70b-versatile"
    completion = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "system", "content": system}] + messages,
        max_tokens=200,
        temperature=0.85,
    )
    return completion.choices[0].message.content.strip(), "Llama 3"

@app.post("/chat-delusion")
async def chat_delusion(req: ChatDelusionRequest):
    loop = asyncio.get_event_loop()
    response, model = await loop.run_in_executor(executor, _chat_delusion, req.messages, req.mode)
    return {"response": response, "model": model}


# ── FEATURE 8: SITUATIONSHIP SURVIVAL TIPS ──────────────────────────────────

class SituationshipTipsRequest(BaseModel):
    score: int
    flagged_questions: list  # list of question strings that were Yes

def _get_situ_tips(score: int, flagged: list) -> list:
    if not flagged:
        prompt = "Someone is in a situationship with 0 red flags. Give 3 short, actionable tips to keep things healthy and move towards a real relationship. Be warm and encouraging. Reply as a JSON array of 3 strings, nothing else."
    else:
        flags_str = "\n".join(f"- {q}" for q in flagged)
        prompt = f"""Someone is in a situationship with these red flags:
{flags_str}

Give exactly 3 specific, actionable survival tips addressing these exact issues. Be direct, Gen-Z friendly, and genuinely helpful. 
Reply as a JSON array of exactly 3 strings, nothing else. Example: ["tip 1", "tip 2", "tip 3"]"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    raw = completion.choices[0].message.content.strip()
    import json, re
    # Extract JSON array even if model adds extra text
    match = re.search(r'\[.*?\]', raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return ["Have an honest conversation about what you both want.", "Set a timeline — if nothing changes in 30 days, reassess.", "Your feelings are valid. Don't shrink yourself for someone who won't commit."]

@app.post("/situationship-tips")
async def situationship_tips(req: SituationshipTipsRequest):
    loop = asyncio.get_event_loop()
    tips = await loop.run_in_executor(executor, _get_situ_tips, req.score, req.flagged_questions)
    return {"tips": tips}