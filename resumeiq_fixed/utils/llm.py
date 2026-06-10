"""
utils/llm.py
Gemini-powered LLM functions for ResumeIQ.
"""

import json
import streamlit as st
from utils.gemini_llm import gemini_chat


def get_model() -> str:
    return st.session_state.get("gemini_model", "gemini-2.5-flash")


def ollama_chat(prompt: str, system: str = "", model: str = None) -> str:
    final_prompt = f"{system}\n\n{prompt}" if system else prompt
    return gemini_chat(final_prompt)


def _clean_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()


def parse_resume(text: str) -> dict:
    system = """You are an expert resume parser. Extract structured information from the resume.
Return ONLY valid JSON with this exact structure:
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

    raw = ollama_chat(f"Parse this resume and return ONLY JSON:\n\n{text}", system=system)
    raw = _clean_json(raw)

    try:
        return json.loads(raw)
    except Exception:
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
    system = """You are a hiring manager and talent matcher. Analyze resume vs job and return ONLY JSON:
{
  "score": 85,
  "matched_skills": [],
  "missing_skills": [],
  "experience_match": "strong|moderate|weak",
  "education_match": "strong|moderate|weak",
  "summary": "",
  "recommendation": "Apply|Consider|Skip"
}"""

    prompt = f"""
Resume:
{json.dumps(resume_data)[:2000]}

Job:
{json.dumps(job)[:1500]}

Return match analysis as JSON.
"""

    raw = ollama_chat(prompt, system=system)
    raw = _clean_json(raw)

    try:
        return json.loads(raw)
    except Exception:
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
    system = """You are a career coach. Analyze skills gaps and return ONLY JSON:
{
  "target_role": "",
  "current_fit_score": 70,
  "gaps": [],
  "strengths": [],
  "quick_wins": [],
  "long_term_goals": [],
  "recommended_certifications": [],
  "action_plan": ""
}"""

    prompt = f"""
Candidate profile:
{json.dumps(resume_data)[:2000]}

Target role: {target_role}

Analyze gaps and provide roadmap. Return JSON.
"""

    raw = ollama_chat(prompt, system=system)
    raw = _clean_json(raw)

    try:
        return json.loads(raw)
    except Exception:
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
    system = f"""You are an expert career coach who writes compelling, personalized cover letters.
Write in a {tone} tone. Return only the cover letter text."""

    prompt = f"""
Candidate:
{json.dumps(resume_data)[:2000]}

Target Job:
{json.dumps(job)[:1500]}

Write a tailored cover letter.
"""

    return ollama_chat(prompt, system=system)


def chat_with_resume(resume_data: dict, user_question: str, chat_history: list) -> str:
    system = f"""You are a helpful career advisor with deep knowledge of the candidate's resume.

Candidate profile:
{json.dumps(resume_data, indent=2)[:2500]}

Be specific, practical, and encouraging."""

    history_text = ""
    for msg in chat_history[-6:]:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
Chat history:
{history_text}

User question:
{user_question}
"""

    return ollama_chat(prompt, system=system)


def check_ollama_status() -> bool:
    import os
    from dotenv import load_dotenv

    load_dotenv()
    return bool(os.getenv("GEMINI_API_KEY"))


def list_ollama_models() -> list:
    return ["gemini-2.5-flash"]