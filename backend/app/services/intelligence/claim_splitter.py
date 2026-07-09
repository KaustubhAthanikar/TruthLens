import spacy


nlp = spacy.load("en_core_web_sm")


def split_claims(text):

    doc = nlp(text)

    claims=[]


    for sent in doc.sents:

        claim = sent.text.strip()


        if len(claim)>2:

            claims.append(claim)


    return claims