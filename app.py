
# app.py — Main Entry Point of Finformation.ai
#
# This file is the conductor — it imports all modules
# and coordinates them to work together.
# Actual logic lives in the imported files.

import streamlit as st
import json
from google import genai

from config import CONFIG
from database import load_database
from ui_header import render_css, render_header, render_footer
from ui_detection import render_detection_tab
from ui_learning import render_learning_tab

# Page configuration
st.set_page_config(
    page_title="Finformation.ai",
    page_icon="shield",
    layout="wide"
)

# Setup Gemini AI client
API_KEY = "AIzaSyDi_lrOV1ZqUnrZEV7CtPQCqELP2ZTmP24"
client = genai.Client(api_key=API_KEY)

# Load learning modules from local JSON file
with open(CONFIG["paths"]["modules"], "r", encoding="utf-8") as f:
    MODULES = json.load(f)

# Load regulatory database into ChromaDB
collection = load_database()

# Initialise all session state variables
for key, val in {
    "analysis_done":       False,
    "show_module":         False,
    "triggered_module_key": None,
    "feedback_given":      False,
    "feedback_text":       "",
    "completed_modules":   [],
    "quiz_scores":         {}
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Render CSS styles and header
render_css()
render_header()

# Create two main tabs
tab1, tab2 = st.tabs([
    "🔍 Fraud Detection",
    "📚 Learning Centre"
])

# Tab 1 — Fraud Detection
with tab1:
    render_detection_tab(client, collection, MODULES)

# Tab 2 — Learning Centre
with tab2:
    render_learning_tab(MODULES)

# Footer
render_footer()
