import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text:str):
    doc = nlp(text)
    entities=[]
    for ent in doc.ents:
        entities.append(ent.text)

    return entities