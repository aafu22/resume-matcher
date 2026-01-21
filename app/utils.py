from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader

from app.model import get_model

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def calculate_similarity(resume_text: str, job_text: str):
    # ✅ load model only when needed (saves memory)
    model = get_model()

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
