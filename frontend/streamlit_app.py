import streamlit as st
import requests

# ✅ Your Render backend URL
BACKEND_BASE = "https://resume-matcher-c1rv.onrender.com"

# ✅ API endpoints
PDF_MATCH_URL = BACKEND_BASE + "/match_resume_pdf"
TEXT_MATCH_URL = BACKEND_BASE + "/match_resume"

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="centered")

st.title("📄 AI Resume Screening / Job Matching System")
st.write("Upload your resume OR paste resume text and match with a job description.")

# ✅ Wake backend button (Render free tier sleeps)
st.subheader("🔄 Backend Status")
if st.button("Wake Backend / Check Status ✅"):
    try:
        r = requests.get(BACKEND_BASE + "/", timeout=30)
        st.success("✅ Backend is awake!")
        st.json(r.json())
    except Exception as e:
        st.error("❌ Backend not responding (may be sleeping or down).")
        st.write(str(e))

st.divider()

# ✅ Input type selection
mode = st.radio("Choose input mode:", ["📄 Upload Resume PDF", "📝 Paste Resume Text"], horizontal=True)

job_description = st.text_area("Paste Job Description", height=180)

st.divider()

if mode == "📄 Upload Resume PDF":
    st.subheader("📄 Resume PDF Upload")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if resume_file is not None:
        st.success(f"✅ Uploaded: {resume_file.name}")

    if st.button("✅ Match Resume (PDF)"):
        if resume_file is None:
            st.warning("Please upload a resume PDF.")
        elif job_description.strip() == "":
            st.warning("Please enter the job description.")
        else:
            with st.spinner("Matching resume with job description..."):
                try:
                    files = {
                        "resume_file": (resume_file.name, resume_file.getvalue(), "application/pdf")
                    }
                    data = {"job_description": job_description}

                    # ✅ Longer timeout for Render free tier / phone
                    response = requests.post(PDF_MATCH_URL, files=files, data=data, timeout=180)

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
                    st.write("Tip: Click 'Wake Backend' and try again.")
                    st.write("Error:", str(e))

else:
    st.subheader("📝 Paste Resume Text")
    resume_text = st.text_area("Paste Resume Text", height=180, placeholder="Paste your resume content here...")

    if st.button("✅ Match Resume (Text)"):
        if resume_text.strip() == "":
            st.warning("Please paste resume text.")
        elif job_description.strip() == "":
            st.warning("Please enter the job description.")
        else:
            with st.spinner("Matching resume with job description..."):
                try:
                    payload = {
                        "resume_text": resume_text,
                        "job_description": job_description
                    }

                    response = requests.post(TEXT_MATCH_URL, json=payload, timeout=120)

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
                    st.write("Tip: Click 'Wake Backend' and try again.")
                    st.write("Error:", str(e))
