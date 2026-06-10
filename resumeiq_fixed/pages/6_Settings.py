import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.llm import check_ollama_status, list_ollama_models
from utils.vector_store import get_job_count

st.set_page_config(page_title="Settings · ResumeIQ", page_icon="⚙️", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2 class="section-title">Settings & Status</h2>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Ollama status
    st.markdown("**🤖 Ollama Configuration**")
    
    ollama_ok = check_ollama_status()
    status_class = "success" if ollama_ok else "warning"
    status_text = "Connected" if ollama_ok else "Not Running"
    status_icon = "✓" if ollama_ok else "⚠"
    
    st.markdown(f"""
    <div class="info-card" style="margin-bottom:1rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="info-label">Ollama Status</div>
                <div class="info-value">http://localhost:11434</div>
            </div>
            <div class="status-badge {status_class}">{status_icon} {status_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not ollama_ok:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); 
                    border-radius:10px; padding:1rem;">
            <div style="font-size:0.85rem; color:#fcd34d; font-weight:600; margin-bottom:0.5rem;">
                How to start Ollama:
            </div>
            <div style="font-size:0.8rem; color:#94a3b8; font-family:monospace;">
                1. Install: https://ollama.ai<br>
                2. Run: <code>ollama serve</code><br>
                3. Pull model: <code>ollama pull llama3.2</code><br>
                4. For embeddings: <code>ollama pull nomic-embed-text</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        models = list_ollama_models()
        if models:
            st.markdown("**Available Models:**")
            for m in models:
                st.markdown(f"""
                <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.15); 
                             border-radius:8px; padding:0.5rem 0.9rem; margin-bottom:0.4rem;
                             font-size:0.82rem; color:#6ee7b7; font-family:monospace;">
                    ● {m}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    
    # Model settings
    st.markdown("**LLM Settings**")
    
    current_model = st.session_state.get("ollama_model", "llama3.2")
    new_model = st.text_input("Active Model", value=current_model, placeholder="e.g. llama3.2")
    if new_model != current_model:
        st.session_state["ollama_model"] = new_model
    
    embed_model = st.text_input("Embedding Model", value="nomic-embed-text", 
                                help="Used for ChromaDB vector search")
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1,
                            help="Higher = more creative, Lower = more precise")

with col_right:
    # Database status
    st.markdown("**🗄️ ChromaDB Status**")
    
    job_count = get_job_count()
    has_resume = bool(st.session_state.get("resume_data"))
    
    st.markdown(f"""
    <div class="info-card">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
            <span class="info-label">Jobs in Database</span>
            <span style="color:#3b82f6; font-weight:700; font-size:1.1rem;">{job_count}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span class="info-label">Resume Loaded</span>
            <span style="color:{'#10b981' if has_resume else '#ef4444'}; font-weight:600;">
                {'Yes' if has_resume else 'No'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    # Session state
    st.markdown("**📦 Current Session**")
    
    session_items = [
        ("Resume Data", "resume_data"),
        ("Gap Analysis", "gap_data"),
        ("Job Results", "job_results"),
        ("Cover Letter", "cover_letter"),
        ("Chat History", "chat_history"),
    ]
    
    for label, key in session_items:
        exists = key in st.session_state and st.session_state[key]
        icon = "✓" if exists else "○"
        color = "#10b981" if exists else "#334155"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; padding:0.4rem 0; 
                    border-bottom:1px solid rgba(255,255,255,0.04);">
            <span style="font-size:0.82rem; color:#64748b;">{label}</span>
            <span style="font-size:0.82rem; color:{color}; font-weight:600;">{icon}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Session Data", use_container_width=True):
        for key in ["resume_data", "raw_resume_text", "gap_data", "job_results", 
                    "cover_letter", "chat_history", "ai_match_0"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Session cleared!")
        st.rerun()
    
    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    
    # About
    st.markdown("""
    <div style="background:#111827; border:1px solid rgba(255,255,255,0.07); 
                border-radius:14px; padding:1.2rem 1.4rem;">
        <div style="font-size:0.82rem; font-weight:600; color:#f1f5f9; margin-bottom:0.8rem;">
            About ResumeIQ
        </div>
        <div style="font-size:0.78rem; color:#64748b; line-height:1.7;">
            ResumeIQ is a local AI-powered career intelligence platform.<br>
            All data stays on your machine — no external APIs, no data sharing.<br><br>
            <strong style="color:#94a3b8;">Stack:</strong> Streamlit · Ollama LLM · ChromaDB · pdfplumber
        </div>
    </div>
    """, unsafe_allow_html=True)
