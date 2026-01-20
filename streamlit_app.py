import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000/match_resume_pdf"

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="centered")

st.title("📄 AI Resume Screening / Job Matching System")
st.write("Upload your Resume (PDF) and paste the Job Description to check the match score.")

# Upload Resume PDF
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job Description Text
job_description = st.text_area("Paste Job Description", height=200)

# Button
if st.button("✅ Match Resume"):
    if resume_file is None:
        st.warning("Please upload a resume PDF.")
    elif job_description.strip() == "":
        st.warning("Please enter job description.")
    else:
        with st.spinner("Matching your resume with job description..."):
            try:
                files = {
                    "resume_file": (resume_file.name, resume_file, "application/pdf")
                }
                data = {
                    "job_description": job_description
                }

                response = requests.post(FASTAPI_URL, files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    score = result["match_score"]
                    level = result["match_level"]

                    st.success("✅ Matching Completed!")
                    st.metric("Match Score (%)", score)
                    st.write(f"### Match Level: **{level}**")

                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.write(response.text)

            except Exception as e:
                st.error("❌ Could not connect to backend!")
                st.write("Make sure FastAPI server is running.")
                st.write("Error:", str(e))
