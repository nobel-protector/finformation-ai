# feedback.py — Feedback handler
#
# PURPOSE:
# Handles user feedback after every fraud analysis.
# Returns thank you message to display to user.

def save_feedback(user_input, fraud_score, verdict, feedback_type, feedback_log_path):
    messages = {
        "helpful":   "✅ Thank you! Your feedback helps improve Finformation.ai. This case has been logged.",
        "not_sure":  "⚠️ Thank you. Our team will review this case. Please verify independently at sebi.gov.in.",
        "incorrect": "❌ Thank you for flagging this. This case has been logged for review to improve accuracy.",
        "fraud":     "🚨 Thank you! This has been flagged as confirmed fraud. Please also report at scores.sebi.gov.in or call 1800 266 7575."
    }
    return {
        "message": messages.get(feedback_type, "Thank you for your feedback!"),
        "saved":   True
    }
