from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from app.schemas import ResumeRequest, ResumeResponse
from app.utils import calculate_similarity, extract_text_from_pdf

app = FastAPI(title="AI Resume Screening API (TF-IDF Version)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ok for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Resume Matching API is running ✅"}

# ✅ Text matching endpoint
@app.post("/match_resume", response_model=ResumeResponse)
def match_resume(data: ResumeRequest):
    score, level = calculate_similarity(data.resume_text, data.job_description)

    return ResumeResponse(
        match_score=score,
        match_level=level
    )

# ✅ PDF matching endpoint
@app.post("/match_resume_pdf", response_model=ResumeResponse)
async def match_resume_pdf(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)

    file_path = os.path.join(temp_folder, resume_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)

    # ✅ delete temp file after reading
    try:
        os.remove(file_path)
    except:
        pass

    score, level = calculate_similarity(resume_text, job_description)

    return ResumeResponse(
        match_score=score,
        match_level=level
    )
