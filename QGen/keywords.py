from keybert import KeyBERT

kw_model = KeyBERT()

def extract_keywords(text):

    keywords = kw_model.extract_keywords(
        text,
        top_n=10,
        stop_words="english"
    )

    return [k[0] for k in keywords]
