import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

model.to(device)

print("Model loaded successfully!")

print("Model Ready!")
