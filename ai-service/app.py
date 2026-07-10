from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

import shutil
import uuid
import os
from services.embedding import create_embedding
from  services.ocr import extract_text_from_image
from services.ocr.social_cleaner import clean_social_text

app = FastAPI()

class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():

    return {"status": "TruthLens AI Service Running"}



@app.post("/embed")
def embed(data: TextRequest):

    embedding = create_embedding(data.text)

    return {"embedding": embedding}



@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):

    filename = f"{uuid.uuid4()}.png"

    with open(filename,"wb") as buffer:

        shutil.copyfileobj(file.file,buffer)

    text = extract_text_from_image(filename)

    os.remove(filename)

    text = clean_social_text(text)

    return {"text": text}