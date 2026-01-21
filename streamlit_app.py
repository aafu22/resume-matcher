import streamlit as st
import requests

# ✅ If running locally
FASTAPI_URL = "https://resume-matcher-c1rv.onrender.com/match_resume_pdf"

# ✅ After deploying backend on Render, change to:
# FASTAPI_URL = "https://your-backend.onrender.com/match_resume_pdf"

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="centered")

st.title("📄 AI Resume Screening / Job Matching System")
st.write("Upload your resume (PDF) and paste the job description to get a match score.")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)

if st.button("✅ Match Resume"):
    if resume_file is None:
        st.warning("Please upload a resume PDF.")
    elif job_description.strip() == "":
        st.warning("Please enter the job description.")
    else:
        with st.spinner("Matching resume with job description..."):
            try:
                files = {
                    "resume_file": (resume_file.name, resume_file, "application/pdf")
                }
                data = {
                    "job_description": job_description
                }

                response = requests.post(FASTAPI_URL, files=files, data=data, timeout=120)


                if response.status_code == 200:
                    result = response.json()

                    st.success("✅ Matching Completed!")
                    st.metric("Match Score (%)", result["match_score"])
                    st.write(f"### Match Level: **{result['match_level']}**")

                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.write(response.text)

            except Exception as e:
                st.error("❌ Could not connect to backend!")
                st.write("Make sure FastAPI server is running.")
                st.write("Error:", str(e))
