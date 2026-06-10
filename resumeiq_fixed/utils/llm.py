"""
utils/llm.py
All interactions with Ollama LLM — parsing, matching, generation.
"""

import json
import requests
import streamlit as st

OLLAMA_BASE = "http://localhost:11434"


def get_model() -> str:
    return st.session_state.get("ollama_model", "llama3.2")


def ollama_chat(prompt: str, system: str = "", model: str = None) -> str:
    """Send a prompt to Ollama and return the text response."""
    model = model or get_model()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/chat",
            json={"model": model, "messages": messages, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to Ollama. Make sure Ollama is running (`ollama serve`)."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def parse_resume(text: str) -> dict:
    """Use LLM to extract structured data from resume text."""
    system = """You are an expert resume parser. Extract structured information from the resume.
Return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{
  "name": "",
  "email": "",
  "phone": "",
  "location": "",
  "summary": "",
  "years_of_experience": 0,
  "education": [{"degree": "", "institution": "", "year": ""}],
  "skills": {
    "technical": [],
    "soft": [],
    "tools": [],
    "languages": []
  },
  "experience": [
    {
      "title": "",
      "company": "",
      "duration": "",
      "description": "",
      "achievements": []
    }
  ],
  "certifications": [],
  "projects": []
}"""

    prompt = f"Parse this resume and return JSON:\n\n{text}"
    raw = ollama_chat(prompt, system=system)

    # Clean markdown fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return partial data
        return {
            "name": "Could not parse",
            "summary": raw[:500],
            "skills": {"technical": [], "soft": [], "tools": [], "languages": []},
            "experience": [],
            "education": [],
            "certifications": [],
            "projects": [],
            "years_of_experience": 0,
        }


def match_resume_to_job(resume_data: dict, job: dict) -> dict:
    """Score how well a resume matches a job description."""
    system = """You are a hiring manager and talent matcher. Analyze resume vs job and return ONLY JSON:
{
  "score": 85,
  "matched_skills": [],
  "missing_skills": [],
  "experience_match": "strong|moderate|weak",
  "education_match": "strong|moderate|weak",
  "summary": "",
  "recommendation": "Apply|Consider|Skip"
}
Score 0-100. Be precise and objective."""

    prompt = f"""
Resume Summary:
Name: {resume_data.get('name')}
Skills: {json.dumps(resume_data.get('skills', {}))}
Experience: {json.dumps(resume_data.get('experience', [])[:3])}
Education: {json.dumps(resume_data.get('education', []))}

Job:
Title: {job.get('title')}
Company: {job.get('company')}
Description: {job.get('description', '')[:800]}
Required Skills: {json.dumps(job.get('required_skills', []))}

Return match analysis as JSON.
"""
    raw = ollama_chat(prompt, system=system)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except:
        return {
            "score": 50,
            "matched_skills": [],
            "missing_skills": [],
            "experience_match": "moderate",
            "education_match": "moderate",
            "summary": raw[:300],
            "recommendation": "Consider",
        }


def analyze_skill_gaps(resume_data: dict, target_role: str) -> dict:
    """Identify skill gaps for a target job role."""
    system = """You are a career coach. Analyze skills gaps and return ONLY JSON:
{
  "target_role": "",
  "current_fit_score": 70,
  "gaps": [
    {
      "skill": "",
      "importance": "critical|important|nice-to-have",
      "learning_path": "",
      "estimated_time": ""
    }
  ],
  "strengths": [],
  "quick_wins": [],
  "long_term_goals": [],
  "recommended_certifications": [],
  "action_plan": ""
}"""

    prompt = f"""
Candidate's current skills: {json.dumps(resume_data.get('skills', {}))}
Experience: {json.dumps(resume_data.get('experience', [])[:3])}
Target role: {target_role}

Analyze gaps and provide a learning roadmap. Return JSON.
"""
    raw = ollama_chat(prompt, system=system)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except:
        return {
            "target_role": target_role,
            "current_fit_score": 60,
            "gaps": [],
            "strengths": [],
            "quick_wins": [],
            "long_term_goals": [],
            "recommended_certifications": [],
            "action_plan": raw[:500],
        }


def generate_cover_letter(resume_data: dict, job: dict, tone: str = "professional") -> str:
    """Generate a tailored cover letter."""
    system = f"""You are an expert career coach who writes compelling, personalized cover letters.
Write in a {tone} tone. The letter should:
- Be 3-4 paragraphs
- Highlight the most relevant experience 
- Show genuine enthusiasm
- Include specific achievements
- Be human and authentic, not templated
Return only the cover letter text, no extra commentary."""

    prompt = f"""
Candidate: {resume_data.get('name')}
Summary: {resume_data.get('summary', '')}
Top Skills: {json.dumps(list(resume_data.get('skills', {}).get('technical', []))[:10])}
Key Experience: {json.dumps(resume_data.get('experience', [])[:2])}

Target Job: {job.get('title')} at {job.get('company')}
Job Description: {job.get('description', '')[:600]}

Write a compelling, tailored cover letter.
"""
    return ollama_chat(prompt, system=system)


def chat_with_resume(resume_data: dict, user_question: str, chat_history: list) -> str:
    """Answer questions about the resume or career."""
    system = f"""You are a helpful career advisor with deep knowledge of the candidate's resume.
Candidate's profile:
{json.dumps(resume_data, indent=2)[:2000]}

Answer questions about their background, provide career advice, suggest improvements, 
and help them present themselves effectively. Be specific, practical, and encouraging."""

    # Build history
    messages_payload = [{"role": "system", "content": system}]
    for msg in chat_history[-6:]:  # Last 3 exchanges
        messages_payload.append({"role": msg["role"], "content": msg["content"]})
    messages_payload.append({"role": "user", "content": user_question})

    model = get_model()
    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/chat",
            json={"model": model, "messages": messages_payload, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"


def check_ollama_status() -> bool:
    """Check if Ollama is running."""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        return resp.status_code == 200
    except:
        return False


def list_ollama_models() -> list:
    """Get available Ollama models."""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        data = resp.json()
        return [m["name"] for m in data.get("models", [])]
    except:
        return []
