
# analysis.py — Track A, B, C analysis functions

import json
from config import CONFIG
from database import query_database

def load_fraud_patterns():
    with open(CONFIG["paths"]["fraud_patterns"], "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["patterns"]

def track_a(user_input):
    # Check if media input
    if any(w in user_input.lower() for w in CONFIG["media_keywords"]):
        return {
            "score": 65,
            "finding": "Media link detected. Commercial deepfake API (Azure/Hive) would assess authenticity in full build.",
            "type": "media"
        }
    return {
        "score": 10,
        "finding": "Text input. No multimedia detected. Deepfake check not applicable.",
        "type": "text"
    }

def track_b_and_c(user_input, collection, client):
    # Step 1 — Get regulatory context from database
    context = query_database(collection, user_input)

    # Step 2 — Load fraud patterns dynamically from JSON
    patterns = load_fraud_patterns()
    pattern_list = ""
    for p in patterns:
        pattern_list += "- " + p["name"] + ": " + p["description"] + "\n"

    # Step 3 — Single combined Gemini call for both Track B and C
    prompt = "You are a SEBI fraud detection and regulatory verification expert.\n\n"
    prompt += "An investor submitted this message:\n"
    prompt += user_input + "\n\n"
    prompt += "TASK 1 — REGULATORY VERIFICATION:\n"
    prompt += "Check this message against these regulatory database records:\n"
    prompt += context + "\n\n"
    prompt += "TASK 2 — FRAUD PATTERN ANALYSIS:\n"
    prompt += "Check this message for these fraud patterns:\n"
    prompt += pattern_list + "\n"
    prompt += "Respond in EXACTLY this format:\n"
    prompt += "TRACK_B_SCORE: [0-100, where 100 = confirmed fraud alert]\n"
    prompt += "TRACK_B_STATUS: [REGISTERED / NOT REGISTERED / NOT FOUND]\n"
    prompt += "TRACK_B_FINDING: [one clear sentence about regulatory status]\n"
    prompt += "TRACK_C_SCORE: [0-100, where 100 = definite fraud]\n"
    prompt += "TRACK_C_PATTERNS: [list fraud patterns found or NONE]\n"
    prompt += "TRACK_C_FINDING: [one clear sentence about fraud patterns]\n"

    response = client.models.generate_content(
        model=CONFIG["gemini_model"],
        contents=prompt
    )
    text = response.text

    # Parse Track B score
    try:
        b_line = [l for l in text.split("\n") if "TRACK_B_SCORE:" in l][0]
        b_score = int("".join(filter(str.isdigit, b_line)))
        b_score = min(100, max(0, b_score))
    except:
        b_score = 50

    # Parse Track C score
    try:
        c_line = [l for l in text.split("\n") if "TRACK_C_SCORE:" in l][0]
        c_score = int("".join(filter(str.isdigit, c_line)))
        c_score = min(100, max(0, c_score))
    except:
        c_score = 50

    # Parse Track B finding
    try:
        b_finding = [l for l in text.split("\n") if "TRACK_B_FINDING:" in l][0]
        b_finding = b_finding.replace("TRACK_B_FINDING:", "").strip()
    except:
        b_finding = text[:200]

    # Parse Track C finding
    try:
        c_finding = [l for l in text.split("\n") if "TRACK_C_FINDING:" in l][0]
        c_finding = c_finding.replace("TRACK_C_FINDING:", "").strip()
    except:
        c_finding = text[:200]

    track_b = {
        "score": b_score,
        "finding": b_finding,
        "context": context
    }

    track_c = {
        "score": c_score,
        "finding": c_finding
    }

    return track_b, track_c

def generate_explanation(user_input, ta, tb, tc, fusion, client):
    prompt = "Help a retail investor in India understand if this investment message is fraudulent.\n"
    prompt += "Message: " + user_input + "\n"
    prompt += "Deepfake Score: " + str(ta["score"]) + "/100\n"
    prompt += "Regulatory Score: " + str(tb["score"]) + "/100\n"
    prompt += "Fraud Pattern Score: " + str(tc["score"]) + "/100\n"
    prompt += "Overall Risk: " + str(fusion["score"]) + "/100 — " + fusion["verdict"] + "\n"
    prompt += "Write exactly 4 simple sentences for a first time retail investor:\n"
    prompt += "1) Is this fraudulent or legitimate and how confident are you?\n"
    prompt += "2) Main reason in plain language — no jargon\n"
    prompt += "3) Exactly what to do next\n"
    prompt += "4) One important safety tip to always remember"
    response = client.models.generate_content(
        model=CONFIG["gemini_model"],
        contents=prompt
    )
    return response.text
