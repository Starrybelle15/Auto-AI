def build_prompt(text, question_type, num_questions, difficulty):
    return f"""
You are an experienced educational assessment expert.

Read the study material below and generate {num_questions} {question_type} questions.

Difficulty: {difficulty}

Rules:
1. Cover the most important concepts.
2. Avoid duplicate questions.
3. Use clear academic English.
4. Number each question.
5. If generating multiple-choice questions:
   - Provide four options (A–D).
   - Mark the correct answer.
6. If generating True/False questions:
   - Include the correct answer.
7. If generating Short Answer questions:
   - Include a brief model answer.

Study Material:

{text}
"""
