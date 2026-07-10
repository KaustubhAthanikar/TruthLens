from fastapi import FastAPI, UploadFile, File
from ocr.ocr_service import extract_text_from_image

import shutil
import uuid
import os


app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "OCR running"
    }


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):

    print("OCR REQUEST RECEIVED:", file.filename)

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    filename = (
        str(uuid.uuid4())
        + "_"
        + file.filename
    )

    path = "uploads/" + filename


    with open(path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    try:

        text = extract_text_from_image(
            path
        )

        print("OCR OUTPUT:", text[:100])


        return {
            "text": text
        }


    except Exception as e:

        print("OCR FAILED:", e)

        raise e


    finally:

        if os.path.exists(path):

            os.remove(path)