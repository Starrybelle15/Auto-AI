PROMPTS = {

"MCQ":

"""
You are an expert educational assessment designer.

Generate exactly {n} multiple-choice questions.

Requirements

• Four options A-D

• Only one correct answer

• Cover the important concepts.

Material

{text}
""",

"SHORT":

"""
Generate exactly {n} short answer questions.

Material

{text}
""",

"TRUE_FALSE":

"""
Generate exactly {n} True or False questions.

Also provide the correct answer.

Material

{text}
""",

"ESSAY":

"""
Generate exactly {n} essay questions.

Material

{text}
"""

}
