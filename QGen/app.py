# ==========================================
# StudyGen AI
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
