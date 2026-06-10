import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.llm import generate_cover_letter

st.set_page_config(page_title="Cover Letter · ResumeIQ", page_icon="✍️", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2 class="section-title">Cover Letter Generator</h2>
</div>
""", unsafe_allow_html=True)

resume_data = st.session_state.get("resume_data")

if not resume_data:
    st.info("👈 Go to **Resume Analyzer** first to upload and analyze your resume.")
    st.stop()

col_form, col_output = st.columns([1, 1], gap="large")

with col_form:
    st.markdown("""
    <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; 
                 letter-spacing:0.1em; font-weight:600; margin-bottom:1rem;">
        Job Details
    </div>
    """, unsafe_allow_html=True)
    
    job_title = st.text_input("Job Title *", placeholder="e.g. Senior Python Developer")
    company = st.text_input("Company Name *", placeholder="e.g. TechCorp Inc.")
    job_desc = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here for a more tailored letter...",
        height=200
    )
    required_skills_input = st.text_input(
        "Key Required Skills",
        placeholder="e.g. Python, Django, AWS, Docker"
    )
    
    tone = st.select_slider(
        "Tone",
        options=["Formal", "Professional", "Confident", "Enthusiastic", "Creative"],
        value="Professional"
    )
    
    include_salary = st.checkbox("Mention salary negotiation", value=False)
    include_remote = st.checkbox("Mention remote/hybrid preference", value=False)
    
    generate_btn = st.button("✍️ Generate Cover Letter", use_container_width=True)

with col_output:
    if generate_btn:
        if not job_title or not company:
            st.error("Please enter at least the job title and company name.")
        else:
            job = {
                "title": job_title,
                "company": company,
                "description": job_desc,
                "required_skills": [s.strip() for s in required_skills_input.split(",") if s.strip()],
            }
            
            extra_notes = []
            if include_salary: extra_notes.append("Mention openness to discuss compensation")
            if include_remote: extra_notes.append("Mention flexibility with remote/hybrid work")
            
            tone_lower = tone.lower()
            
            with st.spinner("✍️ Writing your cover letter..."):
                letter = generate_cover_letter(resume_data, job, tone=tone_lower)
            
            st.session_state["cover_letter"] = letter
            st.session_state["cl_job"] = job
    
    if "cover_letter" in st.session_state:
        letter = st.session_state["cover_letter"]
        job_info = st.session_state.get("cl_job", {})
        
        st.markdown(f"""
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.07); 
                    border-radius:14px; padding:0; overflow:hidden; margin-bottom:1rem;">
            <div style="background:rgba(59,130,246,0.08); border-bottom:1px solid rgba(255,255,255,0.07); 
                        padding:1rem 1.4rem; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.85rem; font-weight:600; color:#f1f5f9;">
                        Cover Letter — {job_info.get('title', '')}
                    </div>
                    <div style="font-size:0.75rem; color:#64748b;">{job_info.get('company', '')}</div>
                </div>
                <div class="status-badge success">✓ Generated</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        edited = st.text_area(
            "Cover Letter (edit as needed)",
            value=letter,
            height=450,
            label_visibility="collapsed"
        )
        
        col_copy, col_regen = st.columns(2)
        with col_copy:
            st.download_button(
                "📥 Download as .txt",
                data=edited,
                file_name=f"cover_letter_{job_info.get('company','').replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_regen:
            if st.button("🔄 Regenerate", use_container_width=True):
                del st.session_state["cover_letter"]
                st.rerun()
    else:
        st.markdown("""
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.07); 
                    border-radius:14px; padding:3rem 2rem; text-align:center; height:400px;
                    display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <div style="font-size:2.5rem; margin-bottom:1rem;">✍️</div>
            <div style="color:#94a3b8; font-size:0.88rem; line-height:1.6;">
                Fill in the job details on the left<br>and click Generate to create a<br>
                personalized cover letter.
            </div>
        </div>
        """, unsafe_allow_html=True)
