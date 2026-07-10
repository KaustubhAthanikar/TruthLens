from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import tempfile
import os

from services.embedding.embedding_service import create_embedding
from services.ocr.ocr_service import extract_text_from_image
from services.ocr.social_cleaner import clean_social_text


app = FastAPI(title="TruthLens AI Service")


class EmbedRequest(BaseModel):
    text: str


@app.get("/")
def health():

    return {
        "status": "running",
        "service": "TruthLens AI"
    }



@app.post("/embed")
def embed(request: EmbedRequest):

    embedding = create_embedding(request.text)

    return {"embedding": embedding}



@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):

    temp_path = f"temp_{file.filename}"

    try:

        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)


        text = extract_text_from_image(temp_path)

        text = clean_social_text(text)

        return {"text": text}


    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)