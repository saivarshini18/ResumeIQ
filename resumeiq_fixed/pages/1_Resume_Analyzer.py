import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.resume_parser import extract_resume_text, clean_text
from utils.llm import parse_resume, check_ollama_status, chat_with_resume
from utils.vector_store import store_resume_embedding

st.set_page_config(page_title="Resume Analyzer · ResumeIQ", page_icon="📄", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

# ── Page Header ──────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2 class="section-title">Resume Analyzer</h2>
</div>
""", unsafe_allow_html=True)

# ── Ollama status ─────────────────────────────────────
if not check_ollama_status():
    st.warning("⚠️ Ollama is not running. Start it with `ollama serve` in your terminal.")

# ── Upload + Parse ────────────────────────────────────
col_upload, col_preview = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📄</div>
        <div class="upload-title">Upload Your Resume</div>
        <div class="upload-sub">PDF, DOCX, or TXT · Max 10MB</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drop resume here", 
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        with st.spinner("🔍 Extracting text..."):
            raw_text = extract_resume_text(uploaded_file)
            raw_text = clean_text(raw_text)
            st.session_state["raw_resume_text"] = raw_text
        
        st.markdown('<div class="status-badge success" style="margin:0.8rem 0;">✓ Text extracted successfully</div>', unsafe_allow_html=True)
        
        with st.expander("📃 View extracted text"):
            st.text_area("Raw text", raw_text, height=200, label_visibility="collapsed")
        
        if st.button("🧠 Analyze with AI", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your resume..."):
                parsed = parse_resume(raw_text)
                st.session_state["resume_data"] = parsed
                store_resume_embedding(parsed, raw_text)
            st.success("✅ Analysis complete!")
            st.rerun()

with col_preview:
    if st.session_state.get("resume_data"):
        data = st.session_state["resume_data"]
        
        # Identity card
        st.markdown(f"""
        <div class="match-card" style="border-color:rgba(59,130,246,0.3);">
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
                <div style="background:linear-gradient(135deg,#3b82f6,#8b5cf6); 
                            width:48px; height:48px; border-radius:14px; 
                            display:flex; align-items:center; justify-content:center;
                            font-size:1.4rem; flex-shrink:0;">👤</div>
                <div>
                    <div style="font-size:1.1rem; font-weight:700; color:#f1f5f9; 
                                font-family:'Space Grotesk',sans-serif;">
                        {data.get('name', 'Unknown')}
                    </div>
                    <div style="font-size:0.78rem; color:#64748b;">
                        {data.get('email', '')} · {data.get('location', '')}
                    </div>
                </div>
            </div>
            <div style="font-size:0.82rem; color:#94a3b8; line-height:1.6;">
                {data.get('summary', '')[:250]}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        exp = data.get("experience", [])
        edu = data.get("education", [])
        skills_count = sum(len(v) for v in data.get("skills", {}).values())
        certs = len(data.get("certifications", []))
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("Experience", f"{data.get('years_of_experience', '?')}y")
        with m2: st.metric("Roles", len(exp))
        with m3: st.metric("Skills", skills_count)
        with m4: st.metric("Certs", certs)
    else:
        st.markdown("""
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.07); 
                    border-radius:14px; padding:3rem; text-align:center; height:100%;">
            <div style="font-size:2rem; margin-bottom:0.8rem;">📊</div>
            <div style="color:#94a3b8; font-size:0.88rem;">
                Upload and analyze a resume to see the parsed profile here.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Detailed Analysis ─────────────────────────────────
if st.session_state.get("resume_data"):
    data = st.session_state["resume_data"]
    
    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    
    tab_skills, tab_exp, tab_edu, tab_chat = st.tabs([
        "🛠️ Skills", "💼 Experience", "🎓 Education", "💬 AI Chat"
    ])
    
    with tab_skills:
        skills = data.get("skills", {})
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Technical Skills**")
            tech = skills.get("technical", [])
            if tech:
                tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in tech])
                st.markdown(f'<div class="skills-container">{tags}</div>', unsafe_allow_html=True)
            
            st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
            st.markdown("**Tools & Platforms**")
            tools = skills.get("tools", [])
            if tools:
                tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in tools])
                st.markdown(f'<div class="skills-container">{tags}</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown("**Soft Skills**")
            soft = skills.get("soft", [])
            if soft:
                tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in soft])
                st.markdown(f'<div class="skills-container">{tags}</div>', unsafe_allow_html=True)
            
            st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
            st.markdown("**Languages**")
            langs = skills.get("languages", [])
            if langs:
                tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in langs])
                st.markdown(f'<div class="skills-container">{tags}</div>', unsafe_allow_html=True)
    
    with tab_exp:
        for i, exp in enumerate(data.get("experience", [])):
            with st.expander(f"**{exp.get('title', 'Role')}** · {exp.get('company', '')}"):
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">Duration</div>
                    <div class="info-value">{exp.get('duration', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Description:** {exp.get('description', '')}")
                achievements = exp.get("achievements", [])
                if achievements:
                    st.markdown("**Key Achievements:**")
                    for ach in achievements:
                        st.markdown(f"• {ach}")
    
    with tab_edu:
        for edu in data.get("education", []):
            st.markdown(f"""
            <div class="info-card">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <div class="info-value">{edu.get('degree', 'Degree')}</div>
                        <div class="info-label">{edu.get('institution', '')}</div>
                    </div>
                    <div class="info-label" style="text-align:right;">{edu.get('year', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        certs = data.get("certifications", [])
        if certs:
            st.markdown("**Certifications**")
            for c in certs:
                st.markdown(f"🏅 {c}")
    
    with tab_chat:
        st.markdown("**Ask AI anything about your resume or career**")
        
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        
        # Display chat
        for msg in st.session_state["chat_history"]:
            role_class = "chat-user" if msg["role"] == "user" else "chat-ai"
            align = "flex-end" if msg["role"] == "user" else "flex-start"
            st.markdown(f"""
            <div style="display:flex; justify-content:{align}; margin-bottom:0.5rem;">
                <div class="chat-bubble {role_class}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        user_q = st.text_input(
            "Ask a question...",
            placeholder="e.g. What are my strongest skills? / How can I improve my resume?",
            key="chat_input"
        )
        
        col_send, col_clear = st.columns([3, 1])
        with col_send:
            if st.button("Send 💬", use_container_width=True) and user_q:
                st.session_state["chat_history"].append({"role": "user", "content": user_q})
                with st.spinner("Thinking..."):
                    response = chat_with_resume(data, user_q, st.session_state["chat_history"])
                st.session_state["chat_history"].append({"role": "assistant", "content": response})
                st.rerun()
        with col_clear:
            if st.button("Clear", use_container_width=True):
                st.session_state["chat_history"] = []
                st.rerun()
