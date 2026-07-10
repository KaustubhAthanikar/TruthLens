from fastapi import APIRouter, UploadFile, File

import shutil
import uuid
import os

from app.services.ai_client import extract_text_from_image
from app.services.claim_service import create_claim

from app.services.ai_client import extract_text_from_image


router = APIRouter(prefix="/api/images",tags=["Images"])


@router.post("/verify")
async def verify_image(image: UploadFile = File(...)):

    os.makedirs("uploads",exist_ok=True)


    filename = (str(uuid.uuid4())+"_"+image.filename)

    path = "uploads/" + filename

    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file,buffer)


    try:

        extracted_text = extract_text_from_image(path)


        processed_text = clean_social_text(extracted_text)


        result = await create_claim(processed_text)


    finally:

        if os.path.exists(path):

            os.remove(path)


    return {

        "extracted_text":extracted_text,

        "processed_text": processed_text,

        "result":result
    }