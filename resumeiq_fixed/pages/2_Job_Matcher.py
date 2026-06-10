import streamlit as st
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.vector_store import search_jobs, get_job_count
from utils.llm import match_resume_to_job

st.set_page_config(page_title="Job Matcher · ResumeIQ", page_icon="💼", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2 class="section-title">Job Matcher</h2>
</div>
""", unsafe_allow_html=True)

resume_data = st.session_state.get("resume_data")
job_count = get_job_count()

# ── Status Bar ────────────────────────────────────────
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    if resume_data:
        st.markdown('<div class="status-badge success">✓ Resume Loaded</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge warning">⚠ No Resume</div>', unsafe_allow_html=True)
with col_s2:
    st.markdown(f'<div class="status-badge info">🗄️ {job_count} Jobs in DB</div>', unsafe_allow_html=True)
with col_s3:
    st.markdown('<div class="status-badge info">🔍 Semantic Search Active</div>', unsafe_allow_html=True)

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

if not resume_data:
    st.info("👈 Go to **Resume Analyzer** first to upload and analyze your resume, then come back for job matching.")
    st.stop()

if job_count == 0:
    st.warning("No jobs in the database. Go to **Job Database** to add jobs.")
    st.stop()

# ── Search Controls ───────────────────────────────────
col_q, col_n = st.columns([3, 1])
with col_q:
    # Build default query from resume
    default_skills = resume_data.get("skills", {}).get("technical", [])[:5]
    default_query = ", ".join(default_skills) if default_skills else "software engineer"
    search_query = st.text_input(
        "Search by skills, role, or keywords",
        value=default_query,
        placeholder="e.g. Python developer, machine learning, React...",
    )
with col_n:
    n_results = st.selectbox("Results", [5, 10, 15, 20], index=1)

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    job_type_filter = st.selectbox("Type", ["All", "Full-time", "Part-time", "Contract", "Remote"])
with col_f2:
    min_score = st.slider("Min Match Score", 0, 100, 30)
with col_f3:
    deep_analysis = st.checkbox("Deep AI Analysis", value=False, help="Use LLM for detailed matching (slower)")

# ── Run Search ────────────────────────────────────────
if st.button("🔍 Find Matching Jobs", use_container_width=True):
    with st.spinner("🔎 Searching jobs semantically..."):
        results = search_jobs(search_query, n_results=n_results)
    
    # Filter
    if job_type_filter != "All":
        results = [j for j in results if job_type_filter.lower() in j.get("type", "").lower()]
    results = [j for j in results if j.get("similarity_score", 0) >= min_score]
    
    st.session_state["job_results"] = results
    st.session_state["deep_analysis"] = deep_analysis

# ── Display Results ───────────────────────────────────
if "job_results" in st.session_state:
    results = st.session_state["job_results"]
    
    if not results:
        st.info("No jobs found matching your criteria. Try adjusting the filters.")
    else:
        st.markdown(f"""
        <div style="margin: 1rem 0 1.2rem 0;">
            <span style="font-size:0.85rem; color:#94a3b8;">Found </span>
            <span style="font-size:0.85rem; color:#f1f5f9; font-weight:600;">{len(results)} matching jobs</span>
        </div>
        """, unsafe_allow_html=True)
        
        for i, job in enumerate(results):
            score = job.get("similarity_score", 0)
            score_class = "high" if score >= 70 else "medium" if score >= 45 else "low"
            score_color = "#10b981" if score >= 70 else "#f59e0b" if score >= 45 else "#ef4444"
            rec = "🟢 Apply" if score >= 70 else "🟡 Consider" if score >= 45 else "🔴 Long Shot"
            
            skills = job.get("required_skills", [])
            skill_tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in skills[:8]])
            
            with st.container():
                st.markdown(f"""
                <div class="match-card {score_class}">
                    <div class="match-header">
                        <div>
                            <div class="match-title">{job.get('title', 'Unknown Role')}</div>
                            <div class="match-company">🏢 {job.get('company', '')} · 
                                📍 {job.get('location', '')} · 
                                💰 {job.get('salary', 'Not specified')}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="match-score {score_class}">{score:.0f}%</div>
                            <div style="font-size:0.72rem; color:#64748b;">{rec}</div>
                        </div>
                    </div>
                    <div style="margin: 0.6rem 0;">
                        <div class="skills-container">{skill_tags}</div>
                    </div>
                    <div style="font-size:0.8rem; color:#64748b; line-height:1.5;">
                        {job.get('description', '')[:200]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_detail, col_analyze = st.columns([3, 1])
                with col_detail:
                    with st.expander("View full description"):
                        st.write(job.get("description", "No description available."))
                        st.markdown(f"**Experience Required:** {job.get('experience_required', 'Not specified')}")
                
                with col_analyze:
                    if st.button(f"🤖 AI Analysis", key=f"analyze_{i}"):
                        with st.spinner("Analyzing match..."):
                            ai_match = match_resume_to_job(resume_data, job)
                        st.session_state[f"ai_match_{i}"] = ai_match
                
                if f"ai_match_{i}" in st.session_state:
                    ai = st.session_state[f"ai_match_{i}"]
                    ai_score = ai.get("score", 0)
                    
                    matched = ai.get("matched_skills", [])
                    missing = ai.get("missing_skills", [])
                    
                    matched_html = " ".join([f'<span class="skill-tag">{s}</span>' for s in matched[:6]])
                    missing_html = " ".join([f'<span class="skill-tag missing">{s}</span>' for s in missing[:6]])
                    
                    st.markdown(f"""
                    <div style="background:rgba(59,130,246,0.05); border:1px solid rgba(59,130,246,0.15); 
                                border-radius:12px; padding:1.2rem; margin-top:0.5rem;">
                        <div style="display:flex; gap:2rem; margin-bottom:1rem;">
                            <div>
                                <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; margin-bottom:0.3rem;">AI Score</div>
                                <div style="font-size:1.5rem; font-weight:700; color:#3b82f6; font-family:'Space Grotesk',sans-serif;">{ai_score}%</div>
                            </div>
                            <div>
                                <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; margin-bottom:0.3rem;">Recommendation</div>
                                <div style="font-size:0.9rem; font-weight:600; color:#f1f5f9;">{ai.get('recommendation', '')}</div>
                            </div>
                        </div>
                        <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.8rem;">{ai.get('summary', '')}</div>
                        <div style="margin-bottom:0.5rem;">
                            <div style="font-size:0.72rem; color:#6ee7b7; text-transform:uppercase; margin-bottom:0.3rem;">✓ Matched Skills</div>
                            <div class="skills-container">{matched_html}</div>
                        </div>
                        <div>
                            <div style="font-size:0.72rem; color:#fca5a5; text-transform:uppercase; margin-bottom:0.3rem;">✗ Missing Skills</div>
                            <div class="skills-container">{missing_html}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div style='height:0.2rem;'></div>", unsafe_allow_html=True)
