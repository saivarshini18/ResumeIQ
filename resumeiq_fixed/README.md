# 🧠 ResumeIQ — AI Resume Analyzer & Job Matcher

A fully local AI-powered career intelligence platform built with Streamlit, Ollama, and ChromaDB.

## Features

| Feature | Description |
|--------|-------------|
| 📄 **Resume Parser** | Upload PDF/DOCX/TXT — AI extracts all structured data |
| 💼 **Job Matcher** | Semantic search matches your profile to jobs in ChromaDB |
| 📊 **Skills Gap** | AI identifies what you're missing for any target role |
| ✍️ **Cover Letter** | Generate tailored cover letters in seconds |
| 🗄️ **Job Database** | Add, manage, and seed job postings |
| ⚙️ **Settings** | Configure model, view status |

## Prerequisites

1. **Python 3.10+**
2. **Ollama** — [https://ollama.ai](https://ollama.ai)

## Setup

### 1. Clone / download the project

```bash
cd resume_analyzer
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

```bash
# In a separate terminal:
ollama serve

# Pull the LLM model (pick one):
ollama pull llama3.2        # Recommended — fast & capable
ollama pull mistral         # Alternative
ollama pull llama3.1        # Larger, more capable

# Pull embedding model for ChromaDB search:
ollama pull nomic-embed-text
```

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

## Usage Flow

1. **Settings** → Check Ollama is connected (green dot)
2. **Job Database** → Click "Seed 10 Sample Jobs" to populate
3. **Resume Analyzer** → Upload your resume → Click "Analyze with AI"
4. **Job Matcher** → Search for matching jobs
5. **Skills Gap** → Pick a target role, see gaps
6. **Cover Letter** → Generate tailored cover letters

## Project Structure

```
resume_analyzer/
├── app.py                    # Main landing page
├── requirements.txt
├── assets/
│   └── style.css             # Full custom dark theme
├── components/
│   ├── header.py             # Top navigation bar
│   └── sidebar.py            # Left sidebar nav
├── pages/
│   ├── 1_Resume_Analyzer.py  # Upload & AI parse
│   ├── 2_Job_Matcher.py      # Semantic job search
│   ├── 3_Skills_Gap.py       # Gap analysis
│   ├── 4_Cover_Letter.py     # Cover letter generation
│   ├── 5_Job_Database.py     # Job CRUD + seeding
│   └── 6_Settings.py         # Config & status
├── utils/
│   ├── llm.py                # All Ollama LLM calls
│   ├── resume_parser.py      # PDF/DOCX text extraction
│   ├── vector_store.py       # ChromaDB operations
│   └── sample_data.py        # 10 sample job postings
└── data/
    └── chroma_db/            # ChromaDB persistent store
```

## Customization

- **Change LLM model**: Sidebar dropdown or Settings page
- **Add your own jobs**: Job Database → Add Job tab
- **Import bulk jobs**: Job Database → Import JSON tab

## Privacy

Everything runs **100% locally**. No data leaves your machine. No API keys needed.
