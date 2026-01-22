# AI Resume Screening / Job Matching System

This project matches a candidate’s Resume with a Job Description and returns a match score and match level.
It helps automate basic resume screening using NLP similarity.

## Features
- Upload Resume PDF and paste Job Description
- (Backup mode) Paste Resume Text (mobile-friendly)
- Returns:
  - Match Score (%)
  - Match Level (Strong / Moderate / Weak)

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: Streamlit
- Similarity: TF-IDF + Cosine Similarity
- Deployment: Render

## Live Links
- Backend Docs: https://resume-matcher-c1rv.onrender.com/docs
- Frontend: https://resume-matcher-1-04fa.onrender.com

## API Endpoints
- `POST /match_resume` (JSON input: resume_text + job_description)
- `POST /match_resume_pdf` (PDF upload + job_description)

## How to Run Locally

### 1) Clone the repository
git clone https://github.com/aafu22/resume-matcher

cd resume-matcher
