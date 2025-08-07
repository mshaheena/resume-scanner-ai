# resume_utils.py

import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization")

# Define skills for different job roles
job_roles = {
    "Data Scientist": ["Python", "Pandas", "Scikit-learn", "Machine Learning", "EDA", "Model Deployment"],
    "ML Engineer": ["Python", "TensorFlow", "PyTorch", "ML Ops", "Deployment", "Data Pipeline"],
    "AI Engineer": ["Transformers", "LLMs", "Hugging Face", "NLP", "Chatbot", "Prompt Engineering"]
}

# Step 1: Extract plain text from uploaded resume PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Step 2: Evaluate match with target job role
def evaluate_resume(text, skills_required):
    text_lower = text.lower()
    matched = [skill for skill in skills_required if skill.lower() in text_lower]
    missing = [skill for skill in skills_required if skill.lower() not in text_lower]
    score = int((len(matched) / len(skills_required)) * 100)
    return score, matched, missing

# Step 3: AI-generated suggestion summary (or fallback)
def suggest_improvements(text):
    try:
        summary = summarizer(text[:1000], max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except:
        return "Consider improving structure, formatting, and highlighting quantified achievements."

# Step 4: Process uploaded resume and return styled markdown output
def process_resume(file, role):
    # Extract job-specific skills
    skills_required = job_roles.get(role, [])

    # Extract and evaluate text
    resume_text = extract_text_from_pdf(file)
    score, matched, missing = evaluate_resume(resume_text, skills_required)
    suggestions = suggest_improvements(resume_text)

    # Final styled Markdown output
    summary = f"""
## 📄 **Resume Summary**

**Selected Role:** `{role}`  
**Score:** `{score}%` match

---

### ✅ **Matched Skills**
`{', '.join(matched) if matched else 'None'}`

### ❌ **Missing Skills**
`{', '.join(missing) if missing else 'None'}`

---

### ✍️ **Suggestions**
{suggestions}

---

### 💡 **Bonus Tip**
Tailor your resume to the specific role by incorporating missing skills, project examples, and relevant metrics to stand out!
"""
    return summary
