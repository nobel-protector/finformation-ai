
# ui_feedback.py — Feedback section

import streamlit as st
from config import CONFIG
from feedback import save_feedback

def render_feedback(user_input, fusion):
    st.markdown("---")
    st.markdown("### 💬 Was this analysis helpful?")
    st.markdown("<div class='feedback-box'>", unsafe_allow_html=True)

    if not st.session_state["feedback_given"]:
        fb1, fb2, fb3, fb4 = st.columns(4)
        feedback_type = None

        with fb1:
            if st.button("✅ Yes helpful", use_container_width=True):
                feedback_type = "helpful"
        with fb2:
            if st.button("⚠️ Not sure", use_container_width=True):
                feedback_type = "not_sure"
        with fb3:
            if st.button("❌ Seems incorrect", use_container_width=True):
                feedback_type = "incorrect"
        with fb4:
            if st.button("🚨 Report fraud", use_container_width=True):
                feedback_type = "fraud"

        if feedback_type:
            result = save_feedback(
                user_input,
                fusion["score"],
                fusion["verdict"],
                feedback_type,
                CONFIG["paths"]["feedback_log"]
            )
            st.session_state["feedback_given"] = True
            st.session_state["feedback_text"] = result["message"]

    if st.session_state["feedback_given"]:
        st.success(st.session_state["feedback_text"])

    st.markdown("</div>", unsafe_allow_html=True)
