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
        timeout=300
    )

    response.raise_for_status()

    return response.json()["embedding"]




def create_embeddings(texts):

    url = f"{settings.EMBEDDING_SERVICE_URL.rstrip('/')}/embed/batch"

    response = requests.post(
        url,
        json={
            "texts": texts
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["embeddings"]





def extract_text_from_image(path):

    url = f"{settings.OCR_SERVICE_URL.rstrip('/')}/ocr"


    with open(path, "rb") as file:

        response = requests.post(
            url,
            files={
                "file": file
            },
            timeout=300
        )


    response.raise_for_status()

    return response.json()["text"]