import requests
from app.config.settings import settings

AI_SERVICE_URL = settings.AI_SERVICE_URL

def create_embedding(text):

    response = requests.post(
        f"{AI_SERVICE_URL}/embed",
        json={"text": text}
    )

    response.raise_for_status()

    return response.json()["embedding"]




def extract_text_from_image(file):

    response = requests.post(
        f"{AI_SERVICE_URL}/ocr",
        files={"file": file}
    )


    response.raise_for_status()


    return response.json()["text"]