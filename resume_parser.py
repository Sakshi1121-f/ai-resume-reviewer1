import docx2txt
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_resume_text(uploaded_file):
    if uploaded_file.name.endswith(".docx"):
        return docx2txt.process(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    return ""

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return set(words)

def get_keyword_match(resume_text, job_desc):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc)
    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    return list(matched), list(missing)

def evaluate_resume(resume_text, job_desc):
    text = [resume_text.lower(), job_desc.lower()]
    vectorizer = CountVectorizer().fit_transform(text)
    score = cosine_similarity(vectorizer)[0][1] * 100
    matched, missing = get_keyword_match(resume_text, job_desc)
    feedback = (
        "Consider adding more job-relevant keywords." if score < 70
        else "Great alignment with the job description!"
    )
    return score, feedback, matched, missing
