
# config.py — All settings in one place

CONFIG = {
    # Gemini model
    "gemini_model": "gemini-2.5-flash",

    # RAG settings
    "max_db_results": 3,

    # Risk thresholds
    "risk_thresholds": {
        "high": 65,
        "moderate": 30
    },

    # Track weights based on input type
    "track_weights": {
        "text":  {"a": 0.10, "b": 0.45, "c": 0.45},
        "media": {"a": 0.40, "b": 0.35, "c": 0.25}
    },

    # Media keywords — triggers Track A weighting
    "media_keywords": [
        "video", "youtube", "instagram", "audio",
        "clip", "telegram", "watch"
    ],

    # File paths
    "paths": {
        "database":         "/content/regulatory_database.csv",
        "modules":          "/content/modules_data.json",
        "keyword_mapping":  "/content/keyword_mapping.json",
        "fraud_patterns":   "/content/fraud_patterns.json",
        "feedback_log":     "/content/drive/MyDrive/Colab Notebooks/Project Finformation/feedback_log.csv"
    },

    # Risk labels
    "risk_labels": {
        "high": {
            "color":   "red",
            "emoji":   "🔴",
            "verdict": "HIGH RISK — Very Likely Fraudulent",
            "action":  "DO NOT INVEST. Report to SEBI SCORES at scores.sebi.gov.in or call 1800 266 7575."
        },
        "moderate": {
            "color":   "amber",
            "emoji":   "🟡",
            "verdict": "MODERATE RISK — Verify Before Acting",
            "action":  "Verify the entity at sebi.gov.in before investing."
        },
        "low": {
            "color":   "green",
            "emoji":   "🟢",
            "verdict": "LOW RISK — Appears Legitimate",
            "action":  "Entity appears legitimate. Always verify on SEBI registry. All investments subject to market risk."
        }
    }
}
