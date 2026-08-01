from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize(text):

    if len(text) < 300:

        return text

    summary = summarizer(
        text[:2500],
        max_length=120,
        min_length=40,
        do_sample=False
    )

    return summary[0]["summary_text"]
