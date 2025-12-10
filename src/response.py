# src/response.py
import os
import json
import random
import re
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Sentence-transformers model (embedding)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Find FAQ file in data/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQ_PATH = None
for fn in ("faqs.json", "faq.json"):
    p = os.path.join(BASE_DIR, "data", fn)
    if os.path.exists(p):
        FAQ_PATH = p
        break

if FAQ_PATH:
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
else:
    faq_data = {"intents": []}

# Build example list and embeddings
examples = []
intent_ref = []
for intent in faq_data.get("intents", []):
    for ex in intent.get("examples", []):
        examples.append(ex)
        intent_ref.append(intent)

example_embeds = (
    embed_model.encode([e.lower() for e in examples], convert_to_tensor=True)
    if examples
    else None
)

SIMILARITY_THRESHOLD = 0.80  # stricter; will call Groq more often


# ---------------- utilities ----------------
def clean_model_text(text: str) -> str:
    """GUI-friendly cleaning: remove HTML tags and normalize markdown fences."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)  # remove HTML tags
    text = text.replace("```", "")  # remove fence markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # italic
    text = re.sub(r"`(.*?)`", r"\1", text)  # inline code markers
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_response(resp):
    """Robust extractor for Groq-style responses (many SDK shapes)."""
    try:
        # object-like with .choices
        if hasattr(resp, "choices"):
            choice0 = resp.choices[0]
            msg = getattr(choice0, "message", None)
            if msg is not None:
                if hasattr(msg, "content"):
                    return msg.content
                if isinstance(msg, dict):
                    return msg.get("content") or msg.get("text")
            if hasattr(choice0, "text"):
                return choice0.text
            if isinstance(choice0, dict):
                return (
                    choice0.get("content")
                    or choice0.get("text")
                    or (choice0.get("message") or {}).get("content")
                )
        # .completions shape
        if hasattr(resp, "completions"):
            comp0 = resp.completions[0]
            if hasattr(comp0, "content"):
                return comp0.content
            if isinstance(comp0, dict):
                return comp0.get("content") or comp0.get("text")
        # dict shape
        if isinstance(resp, dict):
            ch = resp.get("choices") or resp.get("completions")
            if ch and isinstance(ch, list) and len(ch) > 0:
                first = ch[0]
                if isinstance(first, dict):
                    return (
                        (first.get("message") or {}).get("content")
                        or first.get("content")
                        or first.get("text")
                    )
        return None
    except Exception as e:
        print("extract_text_from_response error:", e)
        return None


# ---------------- Groq call ----------------
def ask_groq_llm(user_msg: str) -> str:
    system_prompt = (
        "You are CoreDev Assistant, a friendly and accurate programming assistant created by Nauman Khalid. "
        "If asked who built you, always answer: 'I was built by Nauman Khalid as the CoreDev Assistant.' "
        "Do NOT claim to be Meta, OpenAI, or any other organization. Be concise and provide examples when helpful."
    )
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=450,
            temperature=0.25,
        )
        text = extract_text_from_response(resp)
        return (
            clean_model_text(text) if text else "Sorry — I couldn't generate an answer."
        )
    except Exception as e:
        print("Groq error:", repr(e))
        return "Something went wrong while fetching the smart answer."


# ---------------- main get_response ----------------
def get_response(user_msg: str) -> str:
    """
    1) If FAQ examples exist → semantic search
    2) If high-confidence match and response looks strong → return FAQ response
    3) Otherwise call Groq LLM
    """
    if not examples or example_embeds is None:
        return ask_groq_llm(user_msg)

    user_emb = embed_model.encode(user_msg.lower(), convert_to_tensor=True)
    scores = util.cos_sim(user_emb, example_embeds)[0]
    best_idx = int(scores.argmax().item())
    best_score = float(scores[best_idx].item())

    # When FAQ match is very strong, use it. Otherwise fallback to LLM.
    if best_score >= SIMILARITY_THRESHOLD:
        intent = intent_ref[best_idx]
        resp = random.choice(
            intent.get("responses", ["I don't have a good answer right now."])
        )
        # Reject obviously short or placeholder answers
        if len(resp.strip()) < 30:
            return ask_groq_llm(user_msg)
        # If user's query uses many tokens not present in example (uncommon_ratio), fallback
        ex = examples[best_idx].lower()
        user = user_msg.lower()
        uncommon_ratio = len([w for w in user.split() if w not in ex.split()]) / max(
            1, len(user.split())
        )
        if uncommon_ratio > 0.5:
            return ask_groq_llm(user_msg)
        return resp
    else:
        return ask_groq_llm(user_msg)
