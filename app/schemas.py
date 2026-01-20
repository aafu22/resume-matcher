from pydantic import BaseModel

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

class ResumeResponse(BaseModel):
    match_score: float
    match_level: str
