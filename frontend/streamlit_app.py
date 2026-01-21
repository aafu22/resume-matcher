import streamlit as st
import requests

FASTAPI_URL = "https://resume-matcher-c1rv.onrender.com/match_resume_pdf"

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="centered")

st.title("📄 AI Resume Screening / Job Matching System")
st.write("Upload your resume (PDF) and paste the job description to get a match score.")

# ✅ Keep uploaded file in session
if "resume_file" not in st.session_state:
    st.session_state.resume_file = None

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_uploader")

# ✅ If file uploaded, store it
if uploaded_file is not None:
    st.session_state.resume_file = uploaded_file
    st.success(f"✅ Uploaded: {uploaded_file.name}")

job_description = st.text_area("Paste Job Description", height=200)

if st.button("✅ Match Resume"):
    if st.session_state.resume_file is None:
        st.warning("Please upload a resume PDF.")
    elif job_description.strip() == "":
        st.warning("Please enter the job description.")
    else:
        with st.spinner("Matching resume with job description..."):
            try:
                resume_file = st.session_state.resume_file

                files = {
                    "resume_file": (resume_file.name, resume_file.getvalue(), "application/pdf")
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
                st.write("Error:", str(e))
