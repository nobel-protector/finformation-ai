
# ui_detection.py — Fraud Detection Tab
#
# PURPOSE:
# Controls the Fraud Detection tab of Finformation.ai.
# Handles user input, runs analysis pipeline,
# displays results, feedback, and triggered learning module.

import streamlit as st
import time

from analysis import track_a, track_b_and_c, generate_explanation
from fusion import compute_fusion
from ui_feedback import render_feedback
from ui_learning import render_module_content, render_quiz_score


def render_detection_tab(client, collection, MODULES):

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🔍 Submit Content for Analysis")
        st.markdown(
            "Paste any investment message, WhatsApp forward, "
            "social media post, or promotional text."
        )

        # Text input area
        user_input = st.text_area(
            "",
            height=160,
            placeholder="Example: Invest with XYZ and get guaranteed 40% returns. SEBI approved. Limited slots tonight..."
        )

        # Sample demo buttons
        ca, cb, cc = st.columns(3)
        with ca:
            if st.button("🔴 Fake CIS Fraud"):
                st.session_state["si"] = (
                    "URGENT! Invest with Wealth Multiplier India Pvt Ltd. "
                    "GUARANTEED 40% returns in 6 months. SEBI Approved. "
                    "Only 50 slots left. Wire transfer today. Offer closes TONIGHT!"
                )
                st.session_state["analysis_done"] = False
                st.session_state["show_module"] = False
                st.session_state["feedback_given"] = False

        with cb:
            if st.button("🟢 Legitimate Fund"):
                st.session_state["si"] = (
                    "I want to invest in SBI Mutual Fund through "
                    "monthly SIP of Rs 5000. I checked on AMFI website."
                )
                st.session_state["analysis_done"] = False
                st.session_state["show_module"] = False
                st.session_state["feedback_given"] = False

        with cc:
            if st.button("🔴 Pump and Dump"):
                st.session_state["si"] = (
                    "Hot tip — Zeta Pharma stock will 10x in 3 months. "
                    "Secret FDA deal. Buy quietly before announcement. "
                    "200 people already made lakhs!"
                )
                st.session_state["analysis_done"] = False
                st.session_state["show_module"] = False
                st.session_state["feedback_given"] = False

        # Load sample input if button was clicked
        if "si" in st.session_state and not user_input:
            user_input = st.session_state["si"]

        # Main analyse button
        analyse = st.button(
            "🔍 Analyse for Fraud Risk",
            type="primary",
            use_container_width=True
        )

    with col2:
        # Regulatory databases panel
        st.markdown("### 🏛️ Regulatory Databases")
        st.markdown("*Connected via RAG Architecture*")
        for flag, name, country in [
            ("🇮🇳", "SEBI",   "India"),
            ("🌐",  "IOSCO",  "Global"),
            ("🇬🇧", "FCA",    "UK"),
            ("🇺🇸", "SEC",    "USA"),
            ("🇸🇬", "MAS",    "Singapore"),
            ("🇮🇳", "NSE/BSE","India")
        ]:
            st.markdown(
                f"{flag} **{name}** — {country} &nbsp; 🟢",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### ⚙️ How It Works")
        st.markdown("""
1. 📥 Submit any content
2. 🎥 Track A: Deepfake check
3. 🏛️ Track B: Regulatory verify (RAG)
4. 🧠 Track C: Fraud patterns (LLM)
5. ⚖️ Risk fusion score
6. 💬 Feedback collection
7. 📚 Education module triggered
        """)

    # RUN ANALYSIS when button clicked
    if analyse and user_input and user_input.strip():
        st.session_state["analysis_done"] = False
        st.session_state["show_module"] = False
        st.session_state["feedback_given"] = False

        st.markdown("---")
        st.markdown("### ⚙️ Running Analysis Pipeline...")
        progress = st.progress(0)
        status = st.empty()

        # Step 1 — Parse input
        status.markdown("📥 **Step 1/4:** Parsing and decomposing input...")
        progress.progress(10)
        time.sleep(0.3)

        # Step 2 — Track A
        status.markdown("🎥 **Step 2/4:** Track A — Deepfake Detection...")
        ta = track_a(user_input)
        progress.progress(25)

        # Step 3 — Track B + C combined
        status.markdown(
            "🏛️🧠 **Step 3/4:** Track B + C — "
            "Regulatory Verification and Fraud Pattern Analysis "
            "(Single Gemini Call)..."
        )
        tb, tc = track_b_and_c(user_input, collection, client)
        progress.progress(75)

        # Step 4 — Fusion and explanation
        status.markdown(
            "⚖️ **Step 4/4:** Computing Score and "
            "Generating Plain Language Explanation..."
        )
        fusion = compute_fusion(ta, tb, tc, user_input)
        explanation = generate_explanation(
            user_input, ta, tb, tc, fusion, client
        )
        progress.progress(100)
        status.empty()

        # Save results to session state
        st.session_state["last_ta"] = ta
        st.session_state["last_tb"] = tb
        st.session_state["last_tc"] = tc
        st.session_state["last_fusion"] = fusion
        st.session_state["last_explanation"] = explanation
        st.session_state["last_input"] = user_input
        st.session_state["triggered_module_key"] = fusion["module_key"]
        st.session_state["analysis_done"] = True

    # DISPLAY RESULTS if analysis has been done
    if st.session_state["analysis_done"]:
        fusion      = st.session_state["last_fusion"]
        ta          = st.session_state["last_ta"]
        tb          = st.session_state["last_tb"]
        tc          = st.session_state["last_tc"]
        explanation = st.session_state["last_explanation"]
        saved_input = st.session_state["last_input"]
        triggered   = MODULES.get(
            fusion["module_key"], MODULES["GENERAL"]
        )

        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        # Fraud Probability Score — color coded
        css_map = {
            "red":   "risk-red",
            "amber": "risk-amber",
            "green": "risk-green"
        }
        st.markdown(f"""<div class="{css_map[fusion['color']]}">
            <h1 style="margin:0;font-size:48px">{fusion["emoji"]}</h1>
            <h2 style="margin:8px 0">
                FRAUD PROBABILITY SCORE: {fusion["score"]}%
            </h2>
            <h3 style="margin:0;font-weight:500">
                {fusion["verdict"]}
            </h3>
        </div>""", unsafe_allow_html=True)

        # Track breakdown
        st.markdown("### 📋 Track Breakdown")
        c1, c2, c3 = st.columns(3)
        for col, track, icon, tname in [
            (c1, ta, "🎥", "Deepfake Detection"),
            (c2, tb, "🏛️", "Regulatory Verification"),
            (c3, tc, "🧠", "Fraud Pattern Analysis")
        ]:
            clr = (
                "#c0392b" if track["score"] > 65 else
                "#d97706" if track["score"] > 30 else
                "#1a8c4e"
            )
            with col:
                st.markdown(
                    f"<div class='track-card'>"
                    f"<b>{icon} {tname}</b><br>"
                    f"<h2 style='color:{clr};margin:8px 0'>"
                    f"{track['score']}%</h2>"
                    f"<small>{track['finding'][:120]}...</small>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        # AI plain language explanation
        st.markdown("### 🤖 AI Explanation (Plain Language)")
        st.info(explanation)

        # Recommended action
        st.markdown("### ⚠️ Recommended Action")
        if fusion["color"] == "red":
            st.error("🚨 " + fusion["action"])
        elif fusion["color"] == "amber":
            st.warning("⚠️ " + fusion["action"])
        else:
            st.success("✅ " + fusion["action"])

        # Feedback section
        render_feedback(saved_input, fusion)

        # Triggered learning module box
        st.markdown("---")
        st.markdown(f"""<div class="edu-box">
            <div style="color:#e8a020;font-size:11px;font-weight:700;
                letter-spacing:1px;text-transform:uppercase;
                margin-bottom:8px">
                📚 Triggered Learning Module
            </div>
            <div style="font-size:20px;font-weight:700;margin-bottom:8px">
                {triggered["icon"]} {triggered["title"]}
            </div>
            <div style="color:rgba(255,255,255,0.7);font-size:13px;
                line-height:1.6;margin-bottom:12px">
                {triggered["description"][:300]}...
            </div>
            <div style="color:rgba(255,255,255,0.5);font-size:12px">
                Click the button below to open the full module with quiz
            </div>
        </div>""", unsafe_allow_html=True)

        # Button to open learning module inline
        if not st.session_state["show_module"]:
            if st.button(
                "📚 Open Learning Module — "
                + triggered["icon"] + " "
                + triggered["title"],
                use_container_width=True
            ):
                st.session_state["show_module"] = True

        # Show inline module when button clicked
        if st.session_state["show_module"]:
            mod = triggered
            st.markdown("---")

            # Render module content and quiz
            quiz_answers = render_module_content(
                mod,
                quiz_key_prefix="inline_" + fusion["module_key"]
            )

            # Render quiz score
            render_quiz_score(
                quiz_answers, mod, fusion["module_key"]
            )

    elif analyse:
        st.error("Please enter some text to analyse.")
