import streamlit as st
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.header import render_header
from components.sidebar import render_sidebar
from utils.vector_store import add_job_to_db, get_all_jobs, get_job_count, delete_job
from utils.sample_data import seed_sample_jobs

st.set_page_config(page_title="Job Database · ResumeIQ", page_icon="🗄️", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()
render_sidebar()

st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <h2 class="section-title">Job Database</h2>
</div>
""", unsafe_allow_html=True)

tab_add, tab_view, tab_import = st.tabs(["➕ Add Job", "📋 View All Jobs", "🌱 Seed Sample Data"])

# ── Add Job ───────────────────────────────────────────
with tab_add:
    st.markdown("**Add a new job posting to the vector database**")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Job Title *", placeholder="e.g. Senior Python Developer")
        company = st.text_input("Company *", placeholder="e.g. TechCorp Inc.")
        location = st.text_input("Location", placeholder="e.g. Remote / New York, NY")
        salary = st.text_input("Salary Range", placeholder="e.g. $100,000 - $130,000")
    with col2:
        job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Freelance", "Internship"])
        experience = st.text_input("Experience Required", placeholder="e.g. 3+ years")
        required_skills_raw = st.text_input(
            "Required Skills (comma-separated)",
            placeholder="Python, Django, AWS, Docker, PostgreSQL"
        )
    
    description = st.text_area(
        "Job Description *",
        placeholder="Paste the full job description here...",
        height=180
    )
    
    if st.button("➕ Add Job to Database", use_container_width=True):
        if not job_title or not company or not description:
            st.error("Please fill in at least: Title, Company, and Description")
        else:
            skills_list = [s.strip() for s in required_skills_raw.split(",") if s.strip()]
            job_obj = {
                "title": job_title, "company": company, "location": location,
                "salary": salary, "type": job_type, "experience_required": experience,
                "required_skills": skills_list, "description": description,
            }
            with st.spinner("Adding to ChromaDB..."):
                job_id = add_job_to_db(job_obj)
            st.success(f"✅ Job added! ID: `{job_id}`")

# ── View Jobs ──────────────────────────────────────────
with tab_view:
    job_count = get_job_count()
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
        <div class="status-badge info">🗄️ {job_count} jobs in database</div>
    </div>
    """, unsafe_allow_html=True)
    
    if job_count == 0:
        st.info("No jobs in the database yet. Add jobs manually or seed sample data.")
    else:
        jobs = get_all_jobs()
        
        # Search filter
        search = st.text_input("🔍 Filter by title or company", placeholder="Type to filter...")
        if search:
            jobs = [j for j in jobs if search.lower() in j.get("title","").lower() 
                    or search.lower() in j.get("company","").lower()]
        
        for job in jobs:
            skills = job.get("required_skills", [])
            skill_tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in skills[:6]])
            
            st.markdown(f"""
            <div class="match-card">
                <div class="match-header">
                    <div>
                        <div class="match-title">{job.get('title', '')}</div>
                        <div class="match-company">
                            🏢 {job.get('company', '')} · 
                            📍 {job.get('location', '')} · 
                            💰 {job.get('salary', 'N/A')}
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.72rem; color:#64748b;">{job.get('type', '')}</div>
                        <div style="font-size:0.72rem; color:#64748b;">{job.get('experience_required', '')}</div>
                    </div>
                </div>
                <div class="skills-container" style="margin-top:0.5rem;">{skill_tags}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Seed Data ──────────────────────────────────────────
with tab_import:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">Quick Start</div>
        <div class="info-value">Seed the database with 10 realistic sample job postings</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    This will add 10 sample job postings including:
    - Senior Python Developer, Data Scientist, ML Engineer
    - Full Stack Engineer, DevOps Engineer, NLP Engineer
    - Frontend Engineer, Cybersecurity Analyst, and more
    """)
    
    col_seed, col_clear = st.columns(2)
    with col_seed:
        if st.button("🌱 Seed 10 Sample Jobs", use_container_width=True):
            with st.spinner("Adding sample jobs to ChromaDB..."):
                count = seed_sample_jobs()
            st.success(f"✅ Added {count} sample jobs to the database!")
    
    with col_clear:
        if st.button("⚠️ Clear All Jobs", use_container_width=True):
            st.warning("This will delete all jobs from the database. Use with caution.")
    
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    **Import from JSON file**
    
    Upload a JSON file with an array of job objects. Each job should have:
    `title`, `company`, `description`, `required_skills` (array), `location`, `salary`
    """)
    
    json_file = st.file_uploader("Upload jobs.json", type=["json"])
    if json_file:
        try:
            data = json.loads(json_file.read())
            jobs_to_import = data if isinstance(data, list) else data.get("jobs", [])
            st.info(f"Found {len(jobs_to_import)} jobs to import.")
            if st.button("Import Jobs"):
                imported = 0
                for job in jobs_to_import:
                    try:
                        add_job_to_db(job)
                        imported += 1
                    except Exception as e:
                        st.error(f"Failed: {e}")
                st.success(f"✅ Imported {imported} jobs!")
        except json.JSONDecodeError:
            st.error("Invalid JSON file.")
