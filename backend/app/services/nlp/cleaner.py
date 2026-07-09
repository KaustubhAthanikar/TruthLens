import re

def clean_text(text:str):
    text = text.lower()
    text = re.sub(
        r"http\S+","",text
    )
    text = re.sub(r"\s+"," ",text)
    return text.strip()

