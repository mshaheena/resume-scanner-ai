# app.py
import gradio as gr
from resume_utils import extract_text_from_pdf, evaluate_resume, suggest_improvements

job_roles = {
    "Data Scientist": ["Python", "Machine Learning", "Pandas", "Scikit-learn", "EDA", "Model Deployment"],
    "ML Engineer": ["Deep Learning", "TensorFlow", "PyTorch", "Model Optimization", "MLOps"],
    "Data Analyst": ["SQL", "Excel", "Data Visualization", "Tableau", "Power BI", "Statistics"],
    "Software Developer": ["Java", "C++", "Data Structures", "OOP", "Git", "APIs"]
}

def scan_resume(pdf_file, role):
    text = extract_text_from_pdf(pdf_file)
    score, matched, missing = evaluate_resume(text, job_roles[role])
    suggestions = suggest_improvements(text)

    result = f"""
    ### 📄 Resume Summary
    **Selected Role:** {role}
    
    **Score:** {score}% match

    **Matched Skills:** {', '.join(matched) if matched else 'None'}
    
    **Missing Skills:** {', '.join(missing) if missing else 'None'}

    ### ✍️ Suggestions:
    {suggestions}
    """
    return result

with gr.Blocks() as demo:
    gr.Markdown("""# 🤖 AI Resume Scanner
Upload your resume and select a job role. Get an AI-powered hiring score with feedback.
""")

    with gr.Row():
        pdf_input = gr.File(label="Upload your resume (PDF)")
        job_input = gr.Dropdown(choices=list(job_roles.keys()), label="Select Job Role")

    output = gr.Markdown()
    submit_btn = gr.Button("Scan Resume")
    submit_btn.click(fn=scan_resume, inputs=[pdf_input, job_input], outputs=output)

demo.launch()
