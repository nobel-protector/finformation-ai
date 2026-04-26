
# feedback.py — Save user feedback to Google Drive

import os
import csv
from datetime import datetime

def save_feedback(user_input, fraud_score, verdict, feedback_type, feedback_log_path):
    
    # Define feedback messages shown to user
    messages = {
        "helpful":   "✅ Thank you! Your feedback helps improve Finformation.ai. This case has been logged.",
        "not_sure":  "⚠️ Thank you. Our team will review this case. Please verify independently at sebi.gov.in.",
        "incorrect": "❌ Thank you for flagging this. This case has been logged for review to improve accuracy.",
        "fraud":     "🚨 Thank you! This has been flagged as confirmed fraud. Please also report at scores.sebi.gov.in or call 1800 266 7575."
    }

    # Prepare feedback row
    row = {
        "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query":        user_input[:200],
        "fraud_score":  fraud_score,
        "verdict":      verdict,
        "feedback":     feedback_type
    }

    # Check if file exists
    file_exists = os.path.exists(feedback_log_path)

    # Append to CSV
    try:
        with open(feedback_log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        saved = True
    except Exception as e:
        saved = False

    return {
        "message": messages.get(feedback_type, "Thank you for your feedback!"),
        "saved":   saved
    }
