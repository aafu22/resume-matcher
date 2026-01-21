from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def calculate_similarity(resume_text: str, job_text: str):
    """
    Lightweight similarity using TF-IDF + Cosine Similarity
    ✅ Best for Render free tier (no RAM crash)
    """

    docs = [resume_text, job_text]
    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(docs)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score = round(similarity * 100, 2)

    if score >= 80:
        level = "Strong Match"
    elif score >= 50:
        level = "Moderate Match"
    else:
        level = "Weak Match"

    return score, level
