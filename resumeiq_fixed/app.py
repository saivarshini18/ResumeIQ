import streamlit as st
from components.sidebar import render_sidebar
from components.header import render_header

st.set_page_config(
    page_title="ResumeIQ — AI Resume Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

# Default landing page
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-badge">AI-Powered Career Intelligence</div>
        <h1 class="hero-title">Find Your Perfect<br><span class="accent">Job Match</span></h1>
        <p class="hero-sub">Upload your resume. Let AI analyze your skills, match you to jobs,<br>and give you the edge you need to land your next role.</p>
        <div class="hero-stats">
            <div class="stat-pill">⚡ Powered by Ollama LLM</div>
            <div class="stat-pill">🗄️ ChromaDB Vector Search</div>
            <div class="stat-pill">🎯 Semantic Job Matching</div>
        </div>
    </div>
</div>

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <h3>Resume Parser</h3>
        <p>Deep AI parsing extracts skills, experience, education — structured and ready for matching.</p>
        <span class="feature-tag">→ Upload Resume</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Job Matcher</h3>
        <p>Semantic similarity search finds roles that truly fit your profile, not just keyword hits.</p>
        <span class="feature-tag">→ Match Jobs</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Gap Analysis</h3>
        <p>See exactly what skills are missing for your target role and how to close the gap.</p>
        <span class="feature-tag">→ Analyze Gaps</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">✍️</div>
        <h3>Cover Letter AI</h3>
        <p>Generate tailored cover letters for any job posting in seconds.</p>
        <span class="feature-tag">→ Generate Letter</span>
    </div>
</div>
""", unsafe_allow_html=True)
