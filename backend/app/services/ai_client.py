import requests

from app.config.settings import settings


OCR_SERVICE_URL = settings.OCR_SERVICE_URL

EMBEDDING_SERVICE_URL = settings.EMBEDDING_SERVICE_URL



def create_embedding(text):

    url = f"{settings.EMBEDDING_SERVICE_URL.rstrip('/')}/embed"

    response = requests.post(
        url,
        json={
            "text": text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embedding"]


def extract_text_from_image(path):


    with open(path, "rb") as file:


        response = requests.post(
            f"{OCR_SERVICE_URL}/ocr",
            files={
                "file": file
            },
            timeout=60
        )


    response.raise_for_status()


    return response.json()["text"]