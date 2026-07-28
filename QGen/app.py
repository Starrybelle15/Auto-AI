# ==========================================
# Auto QGen-AI
# AI Question Generator
# ==========================================

import gradio as gr
import torch
import pdfplumber
import os

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

from docx import Document

from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    model.to(device)
    return tokenizer, model
# ------------------------------------------
# Load Model
# ------------------------------------------

MODEL_NAME = "google/flan-t5-small"

print("Loading AI model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"

model.to(device)

print("Model Loaded!")

# ------------------------------------------
# PDF Reader
# ------------------------------------------

def read_pdf(path):

    text = ""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text


# ------------------------------------------
# DOCX Reader
# ------------------------------------------

def read_docx(path):

    document = Document(path)

    paragraphs = []

    for p in document.paragraphs:

        paragraphs.append(p.text)

    return "\n".join(paragraphs)


# ------------------------------------------
# TXT Reader
# ------------------------------------------

def read_txt(path):

    with open(path, "r", encoding="utf8") as f:

        return f.read()

# ------------------------------------------
# Text Cleaner
# ------------------------------------------

def clean_text(text):

    if text is None:
        return ""

    text = text.replace("\n", " ")
    text = " ".join(text.split())

    return text


# ------------------------------------------
# Prompt Builder
# ------------------------------------------

def build_prompt(text, question_type, difficulty, number):

    if question_type == "Short Answer":

        instruction = f"""
Generate exactly {number} short-answer study questions.

For each question also provide a short answer.

Difficulty: {difficulty}
"""

    elif question_type == "Multiple Choice":

        instruction = f"""
Generate exactly {number} multiple-choice questions.

Each question must contain:

A.
B.
C.
D.

Then provide the correct answer.

Difficulty: {difficulty}
"""

    elif question_type == "True / False":

        instruction = f"""
Generate exactly {number} True/False questions.

Provide the correct answer after each one.

Difficulty: {difficulty}
"""

    else:

        instruction = f"""
Generate exactly {number} essay questions.

Difficulty: {difficulty}
"""

    prompt = f"""
You are an experienced university lecturer.

Read the study material carefully.

{instruction}

Study Material

{text}
"""

    return prompt


# ------------------------------------------
# AI Generator
# ------------------------------------------

def generate_questions(text,
                       question_type,
                       difficulty,
                       number):

    text = clean_text(text)

    prompt = build_prompt(
        text,
        question_type,
        difficulty,
        number
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    tokenizer, model = load_model()

    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(

        **inputs,

        max_new_tokens=300,

        temperature=0.7,

        do_sample=True,

        top_p=0.9,

        repetition_penalty=1.2
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

# ------------------------------------------
# Read Uploaded File
# ------------------------------------------

filename = file.name

def extract_text(file):

    if file is None:
        return ""

    if isinstance(file, str):
        filename = file
    else:
        filename = file.name

    extension = os.path.splitext(filename)[1].lower()

    if extension == ".pdf":
        return read_pdf(filename)

    elif extension == ".docx":
        return read_docx(filename)

    elif extension == ".txt":
        return read_txt(filename)

    return ""
# ------------------------------------------
# Main Function
# ------------------------------------------

def process(topic,
            notes,
            file,
            question_type,
            difficulty,
            number):

    text = ""

    if topic:

        text += topic + "\n\n"

    if notes:

        text += notes + "\n\n"

    if file:

        text += extract_text(file)

    if len(text.strip()) == 0:

        return "Please enter a topic, paste notes, or upload a document."

    return generate_questions(
        text,
        question_type,
        difficulty,
        int(number)
    )

# ==========================================
# Gradio Interface
# ==========================================

with gr.Blocks(title="StudyGen AI") as app:

    gr.Markdown(
        """
        # 📚 StudyGen AI
        ### AI-Powered Study Question Generator

        Enter a topic, paste notes, or upload a document.
        """
    )

    with gr.Row():

        topic = gr.Textbox(
            label="Study Topic",
            placeholder="Example: Machine Learning"
        )

        number = gr.Slider(
            minimum=1,
            maximum=20,
            value=5,
            step=1,
            label="Number of Questions"
        )

    notes = gr.Textbox(
        label="Paste Notes",
        lines=10,
        placeholder="Paste lecture notes here..."
    )

    file = gr.File(
        label="Upload PDF, DOCX or TXT",
        file_types=[".pdf", ".docx", ".txt"]
    )

    with gr.Row():

        question_type = gr.Dropdown(
            [
                "Short Answer",
                "Multiple Choice",
                "True / False",
                "Essay"
            ],
            value="Short Answer",
            label="Question Type"
        )

        difficulty = gr.Dropdown(
            [
                "Easy",
                "Medium",
                "Hard"
            ],
            value="Medium",
            label="Difficulty"
        )

    generate = gr.Button(
        "🚀 Generate Questions",
        variant="primary"
    )

    output = gr.Textbox(
        label="Generated Questions",
        lines=20
    )

    generate.click(
        fn=process,
        inputs=[
            topic,
            notes,
            file,
            question_type,
            difficulty,
            number
        ],
        outputs=output
    )

app.launch()
