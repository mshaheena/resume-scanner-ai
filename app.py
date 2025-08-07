# app.py
import gradio as gr
from resume_utils import process_resume

import gradio as gr

custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="emerald",
    neutral_hue="gray",
).set(
    body_background_fill="#f9f9fc",
    button_primary_background_fill="#4f46e5",
    button_primary_text_color="white",
    block_background_fill="white",
    block_shadow="0 4px 12px rgba(0,0,0,0.1)",
    shadow_spread="1px"
)



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

demo = gr.Interface(
    fn=process_resume,
    inputs=[
        gr.File(label="📎 Upload your resume (PDF)", file_types=[".pdf"]),
        gr.Dropdown(choices=["Data Scientist", "ML Engineer", "AI Engineer"], label="🎯 Select Job Role")
    ],
    outputs=[
        gr.Markdown(label="📊 AI Resume Insights")
    ],
    title="🤖 AI Resume Scanner",
    description="Upload your resume and select a job role to get an AI-powered hiring score with feedback.",
    theme=custom_theme
)

if __name__ == "__main__":
    demo.launch()





