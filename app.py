"""
PrepPilot - AI interview practice

Run with:
    streamlit run app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv

from config import APP_ICON, APP_NAME, APP_TAGLINE
from core.agent import ask_agent
from core.evaluator_agent import evaluate_answer
from core.llm import get_api_key
from core.final_coach import generate_coaching_report
from core.report import generate_final_report
from core.session_manager import SessionManager
from interview_bank import INTERVIEW_QUESTIONS
from voice import speak_question

load_dotenv()

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
)

TOTAL_QUESTIONS = len(INTERVIEW_QUESTIONS)


# ---------------------------------
# Session state
# ---------------------------------

def init_state():
    if "session" not in st.session_state:
        st.session_state.session = SessionManager()
    st.session_state.setdefault("started", False)
    st.session_state.setdefault("q_index", 0)
    # Latest evaluation result per question index (survives reruns)
    st.session_state.setdefault("results", {})
    st.session_state.setdefault("coach_chat", [])
    st.session_state.setdefault("final_report", None)


def reset_interview():
    st.session_state.session.clear_session()
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.results = {}
    st.session_state.coach_chat = []
    st.session_state.final_report = None
    for i in range(TOTAL_QUESTIONS):
        st.session_state.pop(f"answer_{i}", None)


init_state()
session: SessionManager = st.session_state.session


# ---------------------------------
# Helpers
# ---------------------------------

def save_evaluation(question, answer, result):
    """Store an evaluation, replacing any earlier one for the same question."""
    history = session.get_history()
    for i, item in enumerate(history):
        if item["question"] == question:
            history.pop(i)
            break
    session.add_evaluation(
        question=question,
        answer=answer,
        tool_results=result["tool_results"],
        feedback=result["feedback"],
    )


def star_badge(found: bool) -> str:
    return "✅" if found else "❌"


def render_result(result: dict):
    tools = result["tool_results"]
    filler = tools.get("detect_filler_words", {})
    star = tools.get("check_star_structure", {})
    relevance = tools.get("score_relevance", {})

    st.markdown("#### Feedback")
    st.info(result["feedback"] or "No feedback returned.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**Filler words**")
        st.metric("Count", filler.get("count", 0))
        words = filler.get("words", [])
        st.caption(", ".join(words) if words else "None detected 🎉")

    with c2:
        st.markdown("**STAR structure**")
        for part in ("situation", "task", "action", "result"):
            st.write(f"{star_badge(star.get(part, False))} {part.capitalize()}")

    with c3:
        st.markdown("**Relevance**")
        score = relevance.get("score", 0)
        st.metric("Score", f"{score}%")
        st.progress(min(max(score, 0), 100) / 100)
        matched = relevance.get("matched_keywords", [])
        st.caption("Matched: " + (", ".join(matched) if matched else "none"))


# ---------------------------------
# Sidebar: progress + live scorecard
# ---------------------------------

with st.sidebar:
    st.title(f"{APP_ICON} {APP_NAME}")
    st.caption(APP_TAGLINE)

    # Resolve the API key: .env / environment -> Streamlit secrets -> sidebar input
    if not get_api_key():
        try:
            secret = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            secret = ""
        if secret:
            os.environ["GROQ_API_KEY"] = secret

    if not get_api_key():
        st.warning("No Groq API key found.")
        entered = st.text_input(
            "Enter your GROQ_API_KEY",
            type="password",
            help="Or put it in a .env file next to app.py: GROQ_API_KEY=your_key",
        )
        if entered.strip():
            os.environ["GROQ_API_KEY"] = entered.strip()
            st.rerun()
        st.caption("Get a free key at https://console.groq.com")
    else:
        st.success("API key loaded", icon="🔑")

    st.divider()
    st.subheader("🔊 Voice")
    voice_on = st.toggle("Read questions aloud", value=True)
    voice_rate = st.slider(
    "Speaking speed", 
    min_value=0.5, 
    max_value=2.0, 
    value=1.0, 
    step=0.25, 
    disabled=not voice_on
)

    st.divider()
    st.subheader("Live Scorecard")

    history = session.get_history()
    if not history:
        st.write("No answers evaluated yet.")
    else:
        report = generate_final_report(history)
        st.metric("Questions answered", f"{report['questions_answered']}/{TOTAL_QUESTIONS}")
        st.metric("Average relevance", f"{report['average_relevance']}%")
        st.metric("Total filler words", report["total_filler_words"])

    st.divider()
    if st.button("🔄 Restart interview", use_container_width=True):
        reset_interview()
        st.rerun()


# ---------------------------------
# Main tabs
# ---------------------------------

tab_practice, tab_coach, tab_report = st.tabs(
    ["📝 Practice", "💬 Ask Coach", "📊 Final Report"]
)

# ---- Practice ----

with tab_practice:
    idx = st.session_state.q_index

    if not st.session_state.started:
        # ---- Welcome screen ----
        st.title(f"👋 Welcome to {APP_NAME}")
        st.markdown(
            f"{APP_TAGLINE}. I'll be your interview coach today."
        )

        st.markdown(
            f"""
**How it works**

1. I ask you **{TOTAL_QUESTIONS} interview questions**, one at a time, from basic to advanced.
2. I **read each question aloud**, and you **type your answer**. Try the STAR method: Situation, Task, Action, Result.
3. You get **instant feedback** on structure, filler words and relevance.
4. Ask the **coach** anything, and finish with a **full report**.
"""
        )

        if voice_on:
            speak_question(
                f"Welcome to {APP_NAME}, your AI interview coach. "
                f"I will ask you interview questions one at a time. "
                f"You can type your answer in the box, and I will give you "
                f"feedback on your structure, filler words and relevance. "
                f"When you are ready, press Start interview.",
                rate=voice_rate,
                autoplay=True,
                key="welcome",
                label="🔊 Click to know more..",
            )

        if st.button("🚀 Start interview", type="primary"):
            st.session_state.started = True
            st.rerun()

    elif idx >= TOTAL_QUESTIONS:
        st.success(
            "🎉 Interview complete! Head to the **Final Report** tab "
            "to see your summary and coaching report."
        )
        if st.button("Review previous question"):
            st.session_state.q_index = TOTAL_QUESTIONS - 1
            st.rerun()
    else:
        current = INTERVIEW_QUESTIONS[idx]
        question = current["question"]

        st.progress(idx / TOTAL_QUESTIONS, text=f"Question {idx + 1} of {TOTAL_QUESTIONS}")
        st.subheader(question)

        if voice_on:
            speak_question(question, rate=voice_rate, autoplay=True, key=f"q{idx}")

        answer_key = f"answer_{idx}"
        answer = st.text_area(
            "Your answer",
            key=answer_key,
            height=220,
            placeholder="Type your interview answer here... (try the STAR method)",
        )

        col_eval, col_prev, col_next = st.columns([2, 1, 1])

        with col_eval:
            evaluate_clicked = st.button(
                "Evaluate Answer", type="primary", use_container_width=True
            )
        with col_prev:
            if st.button("← Previous", disabled=idx == 0, use_container_width=True):
                st.session_state.q_index -= 1
                st.rerun()
        with col_next:
            next_label = "Next →" if idx < TOTAL_QUESTIONS - 1 else "Finish"
            if st.button(next_label, use_container_width=True):
                st.session_state.q_index += 1
                st.rerun()

        if evaluate_clicked:
            if not answer.strip():
                st.warning("Please enter an answer before evaluating.")
            else:
                with st.spinner("Evaluating your answer..."):
                    try:
                        result = evaluate_answer(
                            question=question,
                            answer=answer,
                            expected_keywords=current["expected_keywords"],
                        )
                    except Exception as e:
                        st.error(f"Evaluation failed: {e}")
                    else:
                        save_evaluation(question, answer, result)
                        st.session_state.results[idx] = result
                        st.session_state.final_report = None
                        st.rerun()  # refresh sidebar scorecard

        if idx in st.session_state.results:
            st.divider()
            render_result(st.session_state.results[idx])

# ---- Coach ----

with tab_coach:
    st.subheader("Ask Your Interview Coach")
    st.caption("Ask about your performance so far, e.g. “How am I doing?” or “What's my weakest area?”")

    for msg in st.session_state.coach_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about your performance"):
        st.session_state.coach_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = ask_agent(
                        user_question=prompt,
                        session_history=session.get_history(),
                    )
                except Exception as e:
                    reply = f"Sorry, the coach is unavailable right now: {e}"
            st.markdown(reply)
        st.session_state.coach_chat.append({"role": "assistant", "content": reply})

# ---- Final report ----

with tab_report:
    st.subheader("Final Interview Summary")

    history = session.get_history()

    if not history:
        st.write("No interview answers have been evaluated yet.")
    else:
        if st.button("Generate Final Report", type="primary"):
            with st.spinner("Generating your report and coaching feedback..."):
                final = generate_final_report(history)
                try:
                    coaching = generate_coaching_report(
                        session_history=history, final_report=final
                    )
                except Exception as e:
                    coaching = f"Could not generate the coaching report: {e}"
                st.session_state.final_report = (final, coaching)

        if st.session_state.final_report:
            final, coaching = st.session_state.final_report
            answered = final["questions_answered"]

            m1, m2, m3 = st.columns(3)
            m1.metric("Questions answered", answered)
            m2.metric("Average relevance", f"{final['average_relevance']}%")
            m3.metric("Total filler words", final["total_filler_words"])

            st.markdown("#### Weakest area")
            st.write(f"**Lowest-scoring question:** {final['weakest_question']}")
            st.write(f"**Lowest relevance score:** {final['weakest_score']}%")

            st.markdown("#### STAR components detected")
            s1, s2, s3, s4 = st.columns(4)
            comps = final["star_components"]
            for col, name in zip((s1, s2, s3, s4), ("situation", "task", "action", "result")):
                col.metric(name.capitalize(), f"{comps[name]}/{answered}")

            st.markdown("#### AI Coaching Report")
            st.markdown(coaching)

            st.download_button(
                "⬇️ Download report (.md)",
                data=(
                    f"# {APP_NAME} Report\n\n"
                    f"- Questions answered: {answered}\n"
                    f"- Average relevance: {final['average_relevance']}%\n"
                    f"- Total filler words: {final['total_filler_words']}\n"
                    f"- Weakest question: {final['weakest_question']} "
                    f"({final['weakest_score']}%)\n"
                    f"- STAR coverage: "
                    + ", ".join(f"{k} {v}/{answered}" for k, v in comps.items())
                    + "\n\n## AI Coaching Report\n\n"
                    + coaching
                ),
                file_name=f"{APP_NAME.lower()}_report.md",
                mime="text/markdown",
            )
