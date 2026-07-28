from model import tokenizer, model
from prompts import build_prompt

def generate_questions(text,
                       question_type="Mixed",
                       difficulty="Medium",
                       num_questions=5):

    prompt = build_prompt(
        text,
        question_type,
        num_questions,
        difficulty
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )
