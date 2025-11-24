import os
import json
import random
import openai
from sentence_transformers import SentenceTransformer, util

# Load transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Base project path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Detect correct filename
for name in ["faqs.json", "faq.json"]:
    path = os.path.join(BASE_DIR, "data", name)
    if os.path.exists(path):
        FAQ_PATH = path
        break
else:
    print("⚠ No FAQ file found.")
    FAQ_PATH = None

# Load FAQ data
if FAQ_PATH:
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"intents": []}

# Prepare embeddings
examples = []
intent_ref = []

for intent in data["intents"]:
    for ex in intent["examples"]:
        examples.append(ex)
        intent_ref.append(intent)

if examples:
    example_embeds = model.encode(examples, convert_to_tensor=True)
else:
    example_embeds = None

# ----------------------------------------------------------------------
#   OPENAI FALLBACK - SMART & ENGAGING RESPONSES
# ----------------------------------------------------------------------


def ask_openai(user_msg):
    prompt = f"""
You are CoreDev Assistant — a friendly, highly skilled programming helper created by Nauman Khalid.

Respond in a helpful, engaging developer-friendly style. 
Explain concepts clearly. 
If the user asks something non-technical, respond politely.

User: {user_msg}
Assistant:
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.4,
        )
        return completion["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return "Sorry, I couldn't fetch a smart answer right now."


# ----------------------------------------------------------------------
#   MAIN RESPONSE FUNCTION
# ----------------------------------------------------------------------


def get_response(user_msg):
    # If no FAQs exist, use AI directly
    if not examples:
        return ask_openai(user_msg)

    # Encode input
    user_embed = model.encode(user_msg, convert_to_tensor=True)

    # Calculate similarity
    scores = util.cos_sim(user_embed, example_embeds)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    # If similarity is strong enough → return predefined FAQ answer
    if best_score >= 0.55:  # More strict to reduce wrong matches
        intent = intent_ref[best_idx]
        return random.choice(intent["responses"])

    # Otherwise → fallback to OpenAI
    return ask_openai(user_msg)
