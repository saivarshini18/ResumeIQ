import streamlit as st

def render_header():
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between; 
                padding: 0.8rem 0 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.07); 
                margin-bottom: 1.5rem;">
        <div style="display:flex; align-items:center; gap:0.7rem;">
            <div style="background:linear-gradient(135deg,#3b82f6,#8b5cf6); 
                        width:36px; height:36px; border-radius:10px; 
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.1rem;">🧠</div>
            <div>
                <span style="font-family:'Space Grotesk',sans-serif; font-size:1.15rem; 
                             font-weight:700; color:#f1f5f9; letter-spacing:-0.02em;">ResumeIQ</span>
                <span style="font-size:0.7rem; color:#94a3b8; display:block; 
                             letter-spacing:0.06em; text-transform:uppercase; margin-top:-2px;">
                    AI Career Intelligence
                </span>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:0.6rem;">
            <div style="width:8px; height:8px; background:#10b981; border-radius:50%; 
                        box-shadow:0 0 6px #10b981;"></div>
            <span style="font-size:0.75rem; color:#94a3b8;">Ollama Connected</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
