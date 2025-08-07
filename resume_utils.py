# resume_utils.py
import pdfplumber
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

summarizer = pipeline("summarization")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def evaluate_resume(text, skills_required):
    text_lower = text.lower()
    matched = [skill for skill in skills_required if skill.lower() in text_lower]
    missing = [skill for skill in skills_required if skill.lower() not in text_lower]
    score = int((len(matched) / len(skills_required)) * 100)
    return score, matched, missing

def suggest_improvements(text):
    try:
        summary = summarizer(text[:1000], max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except:
        return "Consider improving structure, formatting, and highlighting quantified achievements."
