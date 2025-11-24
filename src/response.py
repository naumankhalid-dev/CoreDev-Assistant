import os
import json
import random
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer, util

# Load .env
load_dotenv()

# Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Detect FAQ file
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

# Build embeddings
examples = []
intent_ref = []

for intent in data["intents"]:
    for ex in intent["examples"]:
        examples.append(ex)
        intent_ref.append(intent)

example_embeds = model.encode(examples, convert_to_tensor=True) if examples else None


# -------------------------------------------------------------------
#                     GROQ FALLBACK AI ANSWER
# -------------------------------------------------------------------
def ask_ai(user_msg):
    try:
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are CoreDev Assistant — a friendly and engaging programming expert created by Nauman Khalid.",
                },
                {
                    "role": "user",
                    "content": user_msg,
                },
            ],
            max_tokens=200,
            temperature=0.45,
        )

        # FIXED: Groq format
        return chat.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq Error: {e}")
        return "Something went wrong while fetching the smart answer."


# -------------------------------------------------------------------
#                     MAIN RESPONSE LOGIC
# -------------------------------------------------------------------
def get_response(user_msg):
    # No FAQ → use AI directly
    if not examples:
        return ask_ai(user_msg)

    # Encode user input
    user_embed = model.encode(user_msg, convert_to_tensor=True)

    # Compare with FAQ examples
    scores = util.cos_sim(user_embed, example_embeds)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    # If match is strong → return FAQ answer
    if best_score >= 0.55:
        intent = intent_ref[best_idx]
        return random.choice(intent["responses"])

    # Otherwise use Groq AI fallback
    return ask_ai(user_msg)
