
# ui_learning.py — Learning Centre Tab
#
# PURPOSE:
# Controls the Learning Centre tab of Finformation.ai.
# Displays investor education modules, quizzes,
# progress tracking, and quiz scoring.

import streamlit as st


def render_module_content(mod, quiz_key_prefix):
    # Display module title
    st.markdown("## " + mod["icon"] + " " + mod["title"])

    # Display description
    st.markdown("### 📖 About This Topic")
    st.markdown(
        "<div class='module-card'><p style='font-size:14px;line-height:1.8;color:#1a2332'>"
        + mod["description"] + "</p></div>",
        unsafe_allow_html=True
    )

    # Two column layout — left: key facts + red flags
    #                     right: how to verify + real case
    col_l, col_r = st.columns(2)

    with col_l:
        # Key facts section
        st.markdown("### 💡 Key Facts")
        for fact in mod.get("key_facts", []):
            st.markdown(
                "<div class='key-fact'>ℹ️ " + fact + "</div>",
                unsafe_allow_html=True
            )

        # Red flags section
        st.markdown("### 🚨 Red Flags")
        for flag in mod["red_flags"]:
            st.markdown(
                "<div class='red-flag'>⚠️ " + flag + "</div>",
                unsafe_allow_html=True
            )

    with col_r:
        # Verification steps
        st.markdown("### ✅ How to Verify")
        for i, step in enumerate(mod["how_to_verify"], 1):
            st.markdown(
                "<div class='verify-step'>" + str(i) + ". " + step + "</div>",
                unsafe_allow_html=True
            )

        # Real SEBI case example
        if "real_case" in mod:
            st.markdown("### 📋 Real SEBI Case")
            st.markdown(
                "<div class='case-box'>"
                "<div style='font-size:11px;font-weight:700;color:#c0392b;"
                "text-transform:uppercase;margin-bottom:6px'>SEBI Enforcement Case</div>"
                "<div style='font-size:13px;line-height:1.6'>"
                + mod["real_case"] + "</div></div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Quiz section
    st.markdown("### 🧠 Knowledge Quiz — " + str(len(mod["quiz"])) + " Questions")

    quiz_answers = {}
    for i, q in enumerate(mod["quiz"]):
        # Question
        st.markdown("**Q" + str(i+1) + ": " + q["question"] + "**")

        # Answer options
        answer = st.radio(
            "",
            q["options"],
            key=quiz_key_prefix + "_" + str(i),
            index=None
        )
        quiz_answers[i] = answer

        # Show correct or wrong feedback immediately
        if answer is not None:
            if q["options"].index(answer) == q["correct"]:
                st.markdown(
                    "<div class='quiz-correct'>✅ Correct! "
                    + q["explanation"] + "</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='quiz-wrong'>❌ Correct answer: "
                    + q["options"][q["correct"]] + ". "
                    + q["explanation"] + "</div>",
                    unsafe_allow_html=True
                )
        st.markdown("")

    return quiz_answers


def render_quiz_score(quiz_answers, mod, module_key):
    # Only show score when all questions are answered
    answered = [i for i, a in quiz_answers.items() if a is not None]
    if len(answered) == len(mod["quiz"]):

        # Calculate score
        correct_count = sum(
            1 for i, a in quiz_answers.items()
            if a is not None and
            mod["quiz"][i]["options"].index(a) == mod["quiz"][i]["correct"]
        )
        pct = int((correct_count / len(mod["quiz"])) * 100)

        # Determine grade
        grade = "🏆 Excellent!" if pct >= 80 else "👍 Good!" if pct >= 60 else "📖 Keep Learning!"

        # Display score card
        st.markdown(
            "<div class='score-box'>"
            "<div style='font-size:36px'>" + grade + "</div>"
            "<div style='font-size:24px;font-weight:700'>Score: "
            + str(correct_count) + "/" + str(len(mod["quiz"]))
            + " (" + str(pct) + "%)</div></div>",
            unsafe_allow_html=True
        )

        # Save to session state for progress tracking
        if module_key not in st.session_state["completed_modules"]:
            st.session_state["completed_modules"].append(module_key)
        st.session_state["quiz_scores"][module_key] = correct_count

        # Celebrate if excellent score
        if pct >= 80:
            st.balloons()


def render_learning_tab(MODULES):
    st.markdown("## 📚 Investor Learning Centre")
    st.markdown("Browse all modules, build your skills, and track your progress.")

    # Progress tracker
    completed = len(st.session_state["completed_modules"])
    total = len(MODULES)
    st.markdown(f"**Your Progress: {completed}/{total} modules completed**")
    st.progress(completed / total if total > 0 else 0)
    st.markdown("---")

    # Build module dropdown with completion status and scores
    module_keys = list(MODULES.keys())
    module_display = []
    for k in module_keys:
        mod = MODULES[k]
        done = "✅ " if k in st.session_state["completed_modules"] else ""
        score_str = (
            f" [{st.session_state['quiz_scores'][k]}/{len(mod['quiz'])}]"
            if k in st.session_state["quiz_scores"] else ""
        )
        module_display.append(done + mod["icon"] + " " + mod["title"] + score_str)

    # Auto select triggered module from fraud detection
    default_idx = 0
    if st.session_state.get("triggered_module_key"):
        tk = st.session_state["triggered_module_key"]
        if tk in module_keys:
            default_idx = module_keys.index(tk)

    # Module selector dropdown
    selected_display = st.selectbox(
        "Choose a module:",
        module_display,
        index=default_idx
    )
    selected_key = module_keys[module_display.index(selected_display)]
    mod = MODULES[selected_key]

    # Render full module content and quiz
    quiz_answers = render_module_content(
        mod,
        quiz_key_prefix="tab2_" + selected_key
    )

    # Render final score when all questions answered
    render_quiz_score(quiz_answers, mod, selected_key)
