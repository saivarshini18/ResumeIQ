"""
utils/vector_store.py
ChromaDB integration for semantic job search using Ollama embeddings.
"""

import json
import requests
import chromadb
from chromadb.config import Settings
import streamlit as st

OLLAMA_BASE = "http://localhost:11434"
CHROMA_PATH = "./data/chroma_db"


@st.cache_resource
def get_chroma_client():
    """Get or create ChromaDB client (cached)."""
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )
    return client


def get_jobs_collection():
    """Get the jobs collection from ChromaDB."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="jobs",
        metadata={"hnsw:space": "cosine"}
    )


def get_resumes_collection():
    """Get the resumes collection from ChromaDB."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="resumes",
        metadata={"hnsw:space": "cosine"}
    )


def get_ollama_embedding(text: str, model: str = "nomic-embed-text") -> list:
    """Get embedding vector from Ollama."""
    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["embedding"]
    except Exception as e:
        # Fallback: simple hash-based pseudo-embedding for demo
        import hashlib
        import numpy as np
        h = hashlib.md5(text.encode()).hexdigest()
        np.random.seed(int(h[:8], 16) % (2**31))
        return np.random.rand(768).tolist()


def add_job_to_db(job: dict) -> str:
    """Add a job posting to ChromaDB."""
    collection = get_jobs_collection()
    job_id = job.get("id", f"job_{hash(job.get('title','') + job.get('company',''))}")
    
    # Build rich text for embedding
    embed_text = f"""
    Job Title: {job.get('title', '')}
    Company: {job.get('company', '')}
    Description: {job.get('description', '')}
    Required Skills: {', '.join(job.get('required_skills', []))}
    Location: {job.get('location', '')}
    Experience: {job.get('experience_required', '')}
    """
    
    embedding = get_ollama_embedding(embed_text)
    
    collection.upsert(
        ids=[str(job_id)],
        embeddings=[embedding],
        documents=[embed_text],
        metadatas=[{
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": job.get("location", ""),
            "salary": job.get("salary", ""),
            "type": job.get("type", "Full-time"),
            "experience_required": job.get("experience_required", ""),
            "required_skills": json.dumps(job.get("required_skills", [])),
            "description": job.get("description", "")[:500],
        }]
    )
    return str(job_id)


def search_jobs(query_text: str, n_results: int = 10) -> list:
    """Search jobs by semantic similarity."""
    collection = get_jobs_collection()
    
    if collection.count() == 0:
        return []
    
    embedding = get_ollama_embedding(query_text)
    
    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n_results, collection.count()),
        include=["metadatas", "distances", "documents"]
    )
    
    jobs = []
    for i, meta in enumerate(results["metadatas"][0]):
        similarity = 1 - results["distances"][0][i]  # cosine distance → similarity
        job = dict(meta)
        job["similarity_score"] = round(similarity * 100, 1)
        job["required_skills"] = json.loads(meta.get("required_skills", "[]"))
        jobs.append(job)
    
    return sorted(jobs, key=lambda x: x["similarity_score"], reverse=True)


def store_resume_embedding(resume_data: dict, resume_text: str) -> str:
    """Store resume embedding for future matching."""
    collection = get_resumes_collection()
    resume_id = f"resume_{resume_data.get('name', 'unknown').replace(' ', '_')}"
    
    skills_flat = " ".join([
        " ".join(resume_data.get("skills", {}).get("technical", [])),
        " ".join(resume_data.get("skills", {}).get("tools", [])),
    ])
    embed_text = f"""
    Name: {resume_data.get('name')}
    Summary: {resume_data.get('summary', '')}
    Skills: {skills_flat}
    Experience: {json.dumps(resume_data.get('experience', [])[:3])}
    """
    
    embedding = get_ollama_embedding(embed_text)
    
    collection.upsert(
        ids=[resume_id],
        embeddings=[embedding],
        documents=[embed_text],
        metadatas=[{
            "name": resume_data.get("name", ""),
            "email": resume_data.get("email", ""),
            "skills": skills_flat[:500],
            "years_of_experience": str(resume_data.get("years_of_experience", 0)),
        }]
    )
    return resume_id


def get_all_jobs() -> list:
    """Get all jobs from ChromaDB."""
    collection = get_jobs_collection()
    if collection.count() == 0:
        return []
    results = collection.get(include=["metadatas"])
    jobs = []
    for meta in results["metadatas"]:
        job = dict(meta)
        job["required_skills"] = json.loads(meta.get("required_skills", "[]"))
        jobs.append(job)
    return jobs


def delete_job(job_id: str):
    """Delete a job from ChromaDB."""
    collection = get_jobs_collection()
    collection.delete(ids=[job_id])


def get_job_count() -> int:
    """Get total number of jobs in DB."""
    try:
        return get_jobs_collection().count()
    except:
        return 0
