from app.services.translation.translation_service import translate_to_english
from .language_detector import detect_language
from .claim_splitter import split_claims
from .topic_classifier import classify_topic

def analyze_claim(text):

    language = detect_language(text)

    if language != "en":
        processed_text = translate_to_english(
            text
        )
    else:
        processed_text = text

    claims = split_claims(processed_text)

    results=[]

    for claim in claims:

        results.append({

            "claim":claim,

            "topic":classify_topic(claim)

        })


    return {
        "original_language":language,
        "translated_text":processed_text,
        "claims":results
    }