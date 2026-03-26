import streamlit as st
import random
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="IPMAT Generator Pro", layout="wide")
st.title("🎯 IPMAT Indore Full Test Generator")

# INPUTS
col1, col2 = st.columns(2)

with col1:
    total_q = st.number_input("Total Questions", min_value=1, value=10)
    qa_mcq = st.number_input("Quant MCQ", min_value=0, value=4)
    qa_sa = st.number_input("Quant Short Answer", min_value=0, value=3)
    va = st.number_input("Verbal Ability", min_value=0, value=3)

with col2:
    easy = st.number_input("Easy", min_value=0, value=3)
    medium = st.number_input("Medium", min_value=0, value=4)
    hard = st.number_input("Hard", min_value=0, value=3)

topics_input = st.text_input("Topics (comma separated)")
topics = [t.strip() for t in topics_input.split(",") if t.strip()]

options = st.number_input("Options per MCQ", min_value=2, value=4)

# GENERATOR
def generate_question(section, topic, difficulty, options):
    prompt = f"""
Create an IPMAT Indore question.

Section: {section}
Topic: {topic}
Difficulty: {difficulty}

Rules:
- Maintain IPMAT level
- Options must be similar length
- Include traps

Format:
Question:
a.
b.
c.
d.

Correct Answer:
Explanation:
"""
    def generate_question(section, topic, difficulty, options):
    prompt = f"""
Create an IPMAT Indore question.

Section: {section}
Topic: {topic}
Difficulty: {difficulty}

Rules:
- Maintain IPMAT level
- Options must be similar length
- Include traps
- Avoid obvious answers

Format:
Question:
a.
b.
c.
d.

Correct Answer:
Explanation (concise for all options)
"""

    response = model.generate_content(prompt)
    return response.text

# PDF
def generate_pdf(questions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for q in questions:
        pdf.multi_cell(0, 5, q)
    path = "IPMAT_Test.pdf"
    pdf.output(path)
    return path

# MAIN
if st.button("Generate Test"):
    if qa_mcq + qa_sa + va != total_q:
        st.error("Section mismatch")
    elif easy + medium + hard != total_q:
        st.error("Difficulty mismatch")
    elif not topics:
        st.error("Enter topics")
    else:
        difficulty_list = ["Easy"]*easy + ["Medium"]*medium + ["Hard"]*hard
        random.shuffle(difficulty_list)

        section_list = ["QA_MCQ"]*qa_mcq + ["QA_SA"]*qa_sa + ["VA"]*va
        random.shuffle(section_list)

        output = []

        for i in range(total_q):
            topic = random.choice(topics)
            difficulty = difficulty_list[i]
            section = section_list[i]

            st.subheader(f"Q{i+1} ({section} | {topic} | {difficulty})")

            if section == "QA_SA":
                q = f"Create a short answer question on {topic} ({difficulty})"
            else:
                q = generate_question(section, topic, difficulty, options)

            st.write(q)
            output.append(f"Q{i+1}: {q}")

        pdf = generate_pdf(output)

        with open(pdf, "rb") as f:
            st.download_button("Download PDF", f, file_name="IPMAT_Test.pdf")