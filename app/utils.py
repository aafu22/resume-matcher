from sklearn.metrics.pairwise import cosine_similarity
from app.model import get_model
from pypdf import PdfReader
import re

model = get_model()

# ✅ Basic skill database (you can expand)
SKILLS_DB = [
    "python", "java", "c", "c++", "javascript", "typescript",
    "html", "css", "react", "node.js", "express", "mongodb", "mysql",
    "fastapi", "flask", "django",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras",
    "git", "github", "docker", "aws", "linux",
    "data analysis", "pandas", "numpy", "matplotlib",
    "api", "rest", "sql"
]

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text

def extract_skills(text: str):
    text = clean_text(text)
    found = []

    for skill in SKILLS_DB:
        # word boundary matching for safer results
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))

def calculate_similarity(resume_text: str, job_text: str):
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])

    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
    score = round(similarity * 100, 2)

    if score >= 80:
        level = "Strong Match"
    elif score >= 50:
        level = "Moderate Match"
    else:
        level = "Weak Match"

    return score, level

def get_missing_skills(resume_text: str, job_text: str):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_text)

    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    return resume_skills, jd_skills, missing
