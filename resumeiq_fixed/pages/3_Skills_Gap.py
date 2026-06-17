import streamlit as st
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.llm import analyze_skill_gaps

st.set_page_config(
    page_title="Skills Gap · ResumeIQ",
    page_icon="📊",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

st.title("📊 Skills Gap Analysis")

resume_data = st.session_state.get("resume_data")

if not resume_data:
    st.info("👈 Go to Resume Analyzer first and upload a resume.")
    st.stop()

# Role Selection
roles = [
    "AI Engineer",
    "ML Engineer",
    "Data Scientist",
    "Python Developer",
    "Full Stack Developer",
    "Backend Engineer"
]

target_role = st.selectbox(
    "Choose Target Role",
    roles
)

if st.button("Analyze Gaps"):
    with st.spinner("Analyzing..."):
        gap_data = analyze_skill_gaps(
            resume_data,
            target_role
        )

    st.session_state["gap_data"] = gap_data

# Display Results
if "gap_data" in st.session_state:

    gap = st.session_state["gap_data"]

    st.subheader("Current Fit Score")

    fit_score = gap.get("current_fit_score", 0)

    st.progress(min(max(fit_score, 0), 100))
    st.metric("Fit Score", f"{fit_score}%")

    st.subheader("Strengths")

    strengths = gap.get("strengths", [])

    if strengths:
        for s in strengths:
            st.success(s)
    else:
        st.write("No strengths found.")

    st.subheader("Skills Gaps")

    gaps = gap.get("gaps", [])

    normalized_gaps = []

    for item in gaps:

        if isinstance(item, str):
            normalized_gaps.append({
                "skill": item,
                "importance": "important",
                "learning_path": "Recommended learning path",
                "estimated_time": "2-4 weeks"
            })

        elif isinstance(item, dict):
            normalized_gaps.append(item)

    if normalized_gaps:

        for g in normalized_gaps:

            st.markdown(
                f"""
**Skill:** {g.get('skill', 'Unknown')}

- Importance: {g.get('importance', 'important')}
- Learning Path: {g.get('learning_path', 'N/A')}
- Estimated Time: {g.get('estimated_time', 'N/A')}
                """
            )
    else:
        st.write("No skill gaps found.")

    st.subheader("Quick Wins")

    quick_wins = gap.get("quick_wins", [])

    if quick_wins:
        for q in quick_wins:
            st.info(q)

    st.subheader("Recommended Certifications")

    certs = gap.get("recommended_certifications", [])

    if certs:
        for c in certs:
            st.write("🏅", c)

    st.subheader("Long Term Goals")

    goals = gap.get("long_term_goals", [])

    if goals:
        for g in goals:
            st.write("🎯", g)

    st.subheader("Action Plan")

    st.write(gap.get("action_plan", "No action plan available."))
    