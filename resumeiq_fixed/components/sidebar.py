import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 0.5rem 0;">
            <div style="background:linear-gradient(135deg,#3b82f6,#8b5cf6); 
                        width:40px; height:40px; border-radius:12px; 
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.3rem; margin-bottom:0.8rem;">🧠</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.1rem; 
                        font-weight:700; color:#f1f5f9;">ResumeIQ</div>
            <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; 
                        letter-spacing:0.08em;">AI Career Platform</div>
        </div>
        <hr style="border-color:rgba(255,255,255,0.07); margin: 1rem 0;">
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.68rem; color:#475569; text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:0.5rem;">Navigation</div>', unsafe_allow_html=True)

        pages = [
            ("🏠", "Home", "app"),
            ("📄", "Resume Analyzer", "1_Resume_Analyzer"),
            ("💼", "Job Matcher", "2_Job_Matcher"),
            ("📊", "Skills Gap", "3_Skills_Gap"),
            ("✍️", "Cover Letter", "4_Cover_Letter"),
            ("🗄️", "Job Database", "5_Job_Database"),
            ("⚙️", "Settings", "6_Settings"),
        ]

        for icon, label, page in pages:
            st.markdown(f"""
            <a href="/{page}" style="text-decoration:none;">
                <div style="display:flex; align-items:center; gap:0.7rem; 
                            padding:0.55rem 0.75rem; border-radius:9px; 
                            margin-bottom:0.15rem; transition:all 0.15s;
                            background:rgba(255,255,255,0.02); border:1px solid transparent;"
                     onmouseover="this.style.background='rgba(59,130,246,0.1)'; this.style.borderColor='rgba(59,130,246,0.2)'"
                     onmouseout="this.style.background='rgba(255,255,255,0.02)'; this.style.borderColor='transparent'">
                    <span style="font-size:0.95rem;">{icon}</span>
                    <span style="font-size:0.82rem; color:#94a3b8; font-weight:500;">{label}</span>
                </div>
            </a>
            """, unsafe_allow_html=True)

        st.markdown('<hr style="border-color:rgba(255,255,255,0.07); margin: 1rem 0;">', unsafe_allow_html=True)

        # Session state info
        if st.session_state.get("resume_data"):
            st.markdown("""
            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2); 
                        border-radius:10px; padding:0.8rem 1rem;">
                <div style="font-size:0.7rem; color:#6ee7b7; text-transform:uppercase; 
                             letter-spacing:0.08em; font-weight:600; margin-bottom:0.3rem;">
                    ✓ Resume Loaded
                </div>
                <div style="font-size:0.78rem; color:#94a3b8;">Ready for analysis</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.15); 
                        border-radius:10px; padding:0.8rem 1rem;">
                <div style="font-size:0.7rem; color:#93c5fd; text-transform:uppercase; 
                             letter-spacing:0.08em; font-weight:600; margin-bottom:0.3rem;">
                    No Resume
                </div>
                <div style="font-size:0.78rem; color:#64748b;">Upload to get started</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

        # Model selector
        st.markdown('<div style="font-size:0.68rem; color:#475569; text-transform:uppercase; letter-spacing:0.1em; font-weight:600; margin-bottom:0.4rem;">LLM Model</div>', unsafe_allow_html=True)
        model = st.selectbox(
            label="model",
            options=["llama3.2", "llama3.1", "mistral", "codellama", "phi3"],
            label_visibility="collapsed"
        )
        st.session_state["ollama_model"] = model

        st.markdown('<hr style="border-color:rgba(255,255,255,0.07); margin: 1rem 0;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.68rem; color:#1e3a5f; text-align:center;">ResumeIQ v1.0 · Built with Ollama + ChromaDB</div>', unsafe_allow_html=True)
