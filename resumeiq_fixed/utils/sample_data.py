"""
utils/sample_data.py
Seed ChromaDB with sample job postings for demo/testing.
"""

SAMPLE_JOBS = [
    {
        "id": "job_001",
        "title": "Senior Python Developer",
        "company": "TechCorp Inc.",
        "location": "Remote",
        "salary": "$120,000 - $160,000",
        "type": "Full-time",
        "experience_required": "5+ years",
        "required_skills": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API"],
        "description": "We are looking for a Senior Python Developer to join our backend team. You will design and build scalable APIs, work with microservices architecture, and mentor junior developers. Strong experience with Django or FastAPI required. Must have experience with cloud platforms (AWS/GCP) and containerization with Docker and Kubernetes.",
    },
    {
        "id": "job_002",
        "title": "Data Scientist",
        "company": "DataInsights AI",
        "location": "New York, NY",
        "salary": "$130,000 - $170,000",
        "type": "Full-time",
        "experience_required": "3+ years",
        "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL", "Statistics", "Pandas", "scikit-learn"],
        "description": "Join our data science team to build predictive models and derive insights from large datasets. You'll work on NLP, computer vision, and recommendation systems. Strong background in statistics and machine learning algorithms required. Experience with deep learning frameworks preferred.",
    },
    {
        "id": "job_003",
        "title": "Full Stack Engineer",
        "company": "StartupXYZ",
        "location": "San Francisco, CA",
        "salary": "$110,000 - $150,000",
        "type": "Full-time",
        "experience_required": "3+ years",
        "required_skills": ["React", "Node.js", "TypeScript", "PostgreSQL", "GraphQL", "AWS", "Git"],
        "description": "Building the future of fintech at a fast-growing startup. You'll own features end-to-end, from database schema to UI. We use React, Node.js, and AWS. Looking for someone comfortable with ambiguity, able to ship fast, and passionate about clean code.",
    },
    {
        "id": "job_004",
        "title": "Machine Learning Engineer",
        "company": "AI Ventures",
        "location": "Remote",
        "salary": "$140,000 - $190,000",
        "type": "Full-time",
        "experience_required": "4+ years",
        "required_skills": ["Python", "PyTorch", "MLOps", "Kubernetes", "Docker", "AWS SageMaker", "LLMs", "CI/CD"],
        "description": "We're building production ML systems at scale. You'll deploy and monitor ML models, build data pipelines, and work closely with research scientists. Strong Python and MLOps skills required. Experience with LLMs and vector databases is a strong plus.",
    },
    {
        "id": "job_005",
        "title": "DevOps Engineer",
        "company": "CloudFirst Systems",
        "location": "Austin, TX",
        "salary": "$105,000 - $140,000",
        "type": "Full-time",
        "experience_required": "3+ years",
        "required_skills": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD", "Linux", "Python", "Helm"],
        "description": "Own our cloud infrastructure and deployment pipelines. You'll work with Kubernetes clusters, implement GitOps workflows, and ensure 99.99% uptime. Experience with Terraform, AWS, and container orchestration required.",
    },
    {
        "id": "job_006",
        "title": "Frontend Engineer",
        "company": "UXFirst Agency",
        "location": "Remote",
        "salary": "$95,000 - $130,000",
        "type": "Full-time",
        "experience_required": "2+ years",
        "required_skills": ["React", "TypeScript", "CSS", "Figma", "Jest", "Performance Optimization", "Accessibility"],
        "description": "Join our frontend team to build beautiful, performant web applications. You're obsessed with pixel-perfect UI, smooth animations, and accessibility. Deep React and TypeScript experience required. Strong design sensibility preferred.",
    },
    {
        "id": "job_007",
        "title": "Backend Java Engineer",
        "company": "Enterprise Solutions Ltd",
        "location": "Chicago, IL",
        "salary": "$115,000 - $150,000",
        "type": "Full-time",
        "experience_required": "5+ years",
        "required_skills": ["Java", "Spring Boot", "Microservices", "Kafka", "PostgreSQL", "Docker", "REST API"],
        "description": "Design and build enterprise-grade microservices for our financial platform. Experience with Java Spring Boot, Kafka for event streaming, and PostgreSQL required. Must understand distributed systems and have experience with high-throughput applications.",
    },
    {
        "id": "job_008",
        "title": "NLP Engineer",
        "company": "LinguAI Corp",
        "location": "Boston, MA",
        "salary": "$135,000 - $175,000",
        "type": "Full-time",
        "experience_required": "3+ years",
        "required_skills": ["Python", "NLP", "Transformers", "BERT", "spaCy", "LangChain", "Vector Databases", "LLMs"],
        "description": "Build cutting-edge NLP systems including text classification, named entity recognition, and question answering. Deep expertise in Transformers and Hugging Face ecosystem. Experience fine-tuning LLMs and working with vector databases highly valued.",
    },
    {
        "id": "job_009",
        "title": "Product Manager – AI Platform",
        "company": "TechGiant",
        "location": "Seattle, WA",
        "salary": "$150,000 - $200,000",
        "type": "Full-time",
        "experience_required": "5+ years",
        "required_skills": ["Product Management", "AI/ML", "Roadmapping", "Data Analysis", "Agile", "Stakeholder Management"],
        "description": "Lead product strategy for our AI developer platform. You'll work with engineering, design, and business to define and ship impactful features. Strong technical background in AI/ML required. Experience with developer tools or platforms a strong plus.",
    },
    {
        "id": "job_010",
        "title": "Cybersecurity Analyst",
        "company": "SecureNet Inc",
        "location": "Washington, DC",
        "salary": "$100,000 - $135,000",
        "type": "Full-time",
        "experience_required": "3+ years",
        "required_skills": ["Penetration Testing", "SIEM", "Python", "Network Security", "OWASP", "Incident Response", "CISSP"],
        "description": "Protect our infrastructure and customer data. You'll conduct vulnerability assessments, monitor for threats, and lead incident response. Security certifications (CISSP, CEH) preferred. Strong Python scripting for automation required.",
    },
]


def seed_sample_jobs():
    """Load sample jobs into ChromaDB."""
    from utils.vector_store import add_job_to_db
    added = 0
    for job in SAMPLE_JOBS:
        try:
            add_job_to_db(job)
            added += 1
        except Exception as e:
            print(f"Failed to add {job['title']}: {e}")
    return added
