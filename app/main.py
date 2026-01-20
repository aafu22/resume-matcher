from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil

from app.schemas import ResumeRequest, ResumeResponse
from app.utils import calculate_similarity, extract_text_from_pdf

app = FastAPI(title="AI Resume Screening API")

@app.get("/")
def home():
    return {"message": "Resume Matching API is running"}

# Old endpoint (text-based)
@app.post("/match_resume", response_model=ResumeResponse)
def match_resume(data: ResumeRequest):
    score, level = calculate_similarity(data.resume_text, data.job_description)
    return ResumeResponse(match_score=score, match_level=level)


# ✅ NEW endpoint (PDF Resume upload)
@app.post("/match_resume_pdf", response_model=ResumeResponse)
async def match_resume_pdf(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    # Save uploaded PDF temporarily
    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)

    file_path = os.path.join(temp_folder, resume_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_path)

    # Match
    score, level = calculate_similarity(resume_text, job_description)

    return ResumeResponse(match_score=score, match_level=level)
