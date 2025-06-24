import streamlit as st
from src.resume_parser import get_resume_text, evaluate_resume

st.title("📄 AI Resume Reviewer")
st.subheader("Upload your resume and paste a job description to get your ATS score and keyword feedback.")

resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx", "txt"])
job_desc = st.text_area("Paste Job Description")

if resume_file and job_desc:
    resume_text = get_resume_text(resume_file)
    score, feedback, matched, missing = evaluate_resume(resume_text, job_desc)

    st.markdown(f"### ATS Score: **{score:.2f}%**")
    st.write("**Feedback:**", feedback)

    with st.expander("✅ Keywords Found in Resume"):
        st.write(", ".join(matched))

    with st.expander("❌ Keywords Missing from Resume"):
        st.write(", ".join(missing))
