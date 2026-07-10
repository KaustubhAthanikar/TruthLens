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

    print("OCR REQUEST RECEIVED:", file.filename)

    try:

        text = extract_text_from_image(path)

        print("OCR OUTPUT:", text[:100])

        return {
            "text": text
        }

    except Exception as e:

        print("OCR FAILED:", str(e))

        raise e


    finally:

        if os.path.exists(path):
            os.remove(path)