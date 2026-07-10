from fastapi import FastAPI, UploadFile, File
import os

from ocr.ocr_service import extract_text_from_image
from ocr.social_cleaner import clean_social_text


app = FastAPI()


@app.get("/")
def home():

    return {
        "service": "OCR running"
    }



@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):

    path = "temp_" + file.filename

    try:

        with open(path,"wb") as f:
            f.write(await file.read())


        text = extract_text_from_image(path)

        text = clean_social_text(text)


        return {
            "text": text
        }


    finally:

        if os.path.exists(path):
            os.remove(path)