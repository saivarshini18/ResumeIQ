"""
utils/resume_parser.py
Extract text from PDF/DOCX/TXT resumes.
"""

import io
import re
import tempfile
import os


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes using pdfplumber."""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except ImportError:
        return extract_text_pdf_fallback(file_bytes)
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_pdf_fallback(file_bytes: bytes) -> str:
    """Fallback PDF extraction using PyPDF2."""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"PDF extraction failed: {str(e)}"


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes."""
    try:
        import docx
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        doc = docx.Document(tmp_path)
        os.unlink(tmp_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        return f"DOCX extraction failed: {str(e)}"


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Extract text from TXT bytes."""
    try:
        return file_bytes.decode("utf-8").strip()
    except:
        return file_bytes.decode("latin-1").strip()


def extract_resume_text(uploaded_file) -> str:
    """Main entry: extract text from any uploaded resume file."""
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif name.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        return extract_text_from_txt(file_bytes)


def clean_text(text: str) -> str:
    """Clean extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {3,}', ' ', text)
    text = text.strip()
    return text
