from app.services.nlp.cleaner import clean_text
from app.services.nlp.entity_extractor import extract_entities
from app.services.nlp.query_generator import generate_query

text = "NASA confirmed aliens exist in 2026"

cleaned_text = clean_text(text)

entites = extract_entities(cleaned_text)

query = generate_query(cleaned_text,entites)

print(cleaned_text)
print(entites)
print(query)

