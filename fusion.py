
# fusion.py — Risk scoring and module trigger

import json
from config import CONFIG

def load_keyword_mapping():
    with open(CONFIG["paths"]["keyword_mapping"], "r", encoding="utf-8") as f:
        return json.load(f)

def detect_module(user_input):
    keyword_mapping = load_keyword_mapping()
    text_lower = user_input.lower()
    
    # Calculate weighted score for each module
    module_scores = {}
    for module_key, module_data in keyword_mapping.items():
        score = 0
        for keyword, weight in module_data["keywords"].items():
            if keyword in text_lower:
                score += weight
        module_scores[module_key] = score
    
    # Return module with highest score
    best_module = max(module_scores, key=module_scores.get)
    best_score = module_scores[best_module]
    
    # If no keywords matched at all — default based on risk
    if best_score == 0:
        return "CIS"
    
    return best_module

def compute_fusion(ta, tb, tc, user_input):
    # Determine input type
    is_media = any(w in user_input.lower() for w in CONFIG["media_keywords"])
    
    # Apply weights
    weights = CONFIG["track_weights"]["media"] if is_media else CONFIG["track_weights"]["text"]
    composite = int(
        ta["score"] * weights["a"] +
        tb["score"] * weights["b"] +
        tc["score"] * weights["c"]
    )
    composite = min(100, max(0, composite))
    
    # Detect triggered module using weighted keywords
    module_key = detect_module(user_input)
    
    # Determine risk level
    thresholds = CONFIG["risk_thresholds"]
    if composite > thresholds["high"]:
        risk = CONFIG["risk_labels"]["high"]
    elif composite > thresholds["moderate"]:
        risk = CONFIG["risk_labels"]["moderate"]
    else:
        risk = CONFIG["risk_labels"]["low"]
    
    return {
        "score":      composite,
        "color":      risk["color"],
        "verdict":    risk["verdict"],
        "emoji":      risk["emoji"],
        "action":     risk["action"],
        "module_key": module_key
    }
