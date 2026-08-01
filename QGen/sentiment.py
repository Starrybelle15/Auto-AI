from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def analyze_sentiment(text):

    result = classifier(text[:512])[0]

    return {
        "label": result["label"],
        "score": round(result["score"],3)
    }
