import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.llm import analyze_skill_gaps

st.set_page_config(page_title="Skills Gap · ResumeIQ", page_icon="📊", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2 class="section-title">Skills Gap Analysis</h2>
</div>
""", unsafe_allow_html=True)

resume_data = st.session_state.get("resume_data")

if not resume_data:
    st.info("👈 Go to **Resume Analyzer** first to upload and analyze your resume.")
    st.stop()

# ── Target Role Input ─────────────────────────────────
col_role, col_btn = st.columns([3, 1])
with col_role:
    common_roles = [
        "Senior Python Developer", "Data Scientist", "ML Engineer",
        "Full Stack Engineer", "DevOps Engineer", "Frontend Engineer",
        "Product Manager", "Data Engineer", "AI Engineer", "Backend Engineer"
    ]
    target_role = st.selectbox(
        "Select or type a target role",
        options=common_roles,
        index=0
    )
    custom_role = st.text_input(
        "Or enter a custom role",
        placeholder="e.g. Principal Software Architect"
    )
    final_role = custom_role if custom_role else target_role

with col_btn:
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    run_analysis = st.button("📊 Analyze Gaps", use_container_width=True)

if run_analysis:
    with st.spinner(f"🤖 Analyzing gaps for {final_role}..."):
        gap_data = analyze_skill_gaps(resume_data, final_role)
    st.session_state["gap_data"] = gap_data
    st.session_state["gap_role"] = final_role

# ── Display Gap Analysis ──────────────────────────────
if "gap_data" in st.session_state:
    gap = st.session_state["gap_data"]
    role = st.session_state.get("gap_role", "Target Role")
    
    # Header metrics
    fit_score = gap.get("current_fit_score", 0)
    score_color = "#10b981" if fit_score >= 70 else "#f59e0b" if fit_score >= 45 else "#ef4444"
    
    st.markdown(f"""
    <div class="match-card" style="border-color:rgba(59,130,246,0.3); margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div>
                <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; 
                             letter-spacing:0.08em; margin-bottom:0.4rem;">Current Fit</div>
                <div style="font-family:'Space Grotesk',sans-serif; font-size:2.5rem; 
                             font-weight:800; color:{score_color};">{fit_score}%</div>
                <div style="font-size:0.82rem; color:#94a3b8;">for {role}</div>
            </div>
            <div style="text-align:right; max-width:60%;">
                <div style="font-size:0.82rem; color:#94a3b8; line-height:1.6;">
                    {gap.get('action_plan', '')[:300]}
                </div>
            </div>
        </div>
        <div style="margin-top:1rem;">
            <div class="progress-track">
                <div class="progress-fill" style="width:{fit_score}%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        # Strengths
        strengths = gap.get("strengths", [])
        if strengths:
            st.markdown("""
            <div style="font-size:0.72rem; color:#6ee7b7; text-transform:uppercase; 
                         letter-spacing:0.08em; font-weight:600; margin-bottom:0.6rem;">
                ✓ Your Strengths
            </div>
            """, unsafe_allow_html=True)
            tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in strengths])
            st.markdown(f'<div class="skills-container">{tags}</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        
        # Quick wins
        quick_wins = gap.get("quick_wins", [])
        if quick_wins:
            st.markdown("""
            <div style="font-size:0.72rem; color:#fcd34d; text-transform:uppercase; 
                         letter-spacing:0.08em; font-weight:600; margin-bottom:0.6rem;">
                ⚡ Quick Wins (2–4 weeks)
            </div>
            """, unsafe_allow_html=True)
            for qw in quick_wins:
                st.markdown(f"""
                <div style="background:rgba(245,158,11,0.07); border:1px solid rgba(245,158,11,0.2); 
                             border-radius:8px; padding:0.6rem 0.9rem; margin-bottom:0.4rem;
                             font-size:0.82rem; color:#fcd34d;">
                    ⚡ {qw}
                </div>
                """, unsafe_allow_html=True)
        
        # Certifications
        certs = gap.get("recommended_certifications", [])
        if certs:
            st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem; color:#93c5fd; text-transform:uppercase; 
                         letter-spacing:0.08em; font-weight:600; margin-bottom:0.6rem;">
                🏅 Recommended Certifications
            </div>
            """, unsafe_allow_html=True)
            for cert in certs:
                st.markdown(f"🏅 {cert}")
    
    with col_right:
        # Skills gaps
        gaps_list = gap.get("gaps", [])
        if gaps_list:
            st.markdown("""
            <div style="font-size:0.72rem; color:#fca5a5; text-transform:uppercase; 
                         letter-spacing:0.08em; font-weight:600; margin-bottom:0.6rem;">
                ✗ Skills to Develop
            </div>
            """, unsafe_allow_html=True)
            
            importance_order = {"critical": 0, "important": 1, "nice-to-have": 2}
            gaps_sorted = sorted(gaps_list, key=lambda x: importance_order.get(x.get("importance", ""), 3))
            
            for g in gaps_sorted:
                imp = g.get("importance", "nice-to-have")
                imp_color = {"critical": "#ef4444", "important": "#f59e0b", "nice-to-have": "#64748b"}.get(imp, "#64748b")
                imp_bg = {"critical": "rgba(239,68,68,0.08)", "important": "rgba(245,158,11,0.08)", "nice-to-have": "rgba(100,116,139,0.08)"}.get(imp, "")
                
                st.markdown(f"""
                <div style="background:{imp_bg}; border:1px solid {imp_color}33; 
                             border-radius:10px; padding:0.9rem 1rem; margin-bottom:0.6rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <div style="font-size:0.88rem; font-weight:600; color:#f1f5f9;">{g.get('skill', '')}</div>
                        <div style="font-size:0.68rem; color:{imp_color}; text-transform:uppercase; 
                                     font-weight:600; letter-spacing:0.05em;">{imp}</div>
                    </div>
                    <div style="font-size:0.78rem; color:#94a3b8; margin-bottom:0.3rem;">
                        📚 {g.get('learning_path', '')}
                    </div>
                    <div style="font-size:0.72rem; color:#64748b;">⏱ {g.get('estimated_time', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Long term goals
        lt_goals = gap.get("long_term_goals", [])
        if lt_goals:
            st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem; color:#c4b5fd; text-transform:uppercase; 
                         letter-spacing:0.08em; font-weight:600; margin-bottom:0.6rem;">
                🎯 Long-term Goals
            </div>
            """, unsafe_allow_html=True)
            for g in lt_goals:
                st.markdown(f"""
                <div style="background:rgba(139,92,246,0.07); border:1px solid rgba(139,92,246,0.2); 
                             border-radius:8px; padding:0.6rem 0.9rem; margin-bottom:0.4rem;
                             font-size:0.82rem; color:#c4b5fd;">
                    🎯 {g}
                </div>
                """, unsafe_allow_html=True)
