import spacy

nlp = spacy.load("en_core_web_sm")

def generate_query(text,entites):
    doc = nlp(text)
    keywords=[]
    for token in doc:
        if token.pos_ in ["NOUN","PROPN","VERB","ADJ"]:
            keywords.append(token.text)

    words = (entites+keywords)

    query = " ".join(list(set(words)))

    return query