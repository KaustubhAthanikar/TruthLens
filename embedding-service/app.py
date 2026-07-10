from fastapi import FastAPI
from pydantic import BaseModel

from embedding.embedding_service import create_embedding


app = FastAPI()


class EmbedRequest(BaseModel):

    text: str



@app.get("/")
def home():

    return {"service": "TruthLens Embedding Service running"}



@app.post("/embed")
def embed(req: EmbedRequest):

    embedding = create_embedding(req.text)

    return {"embedding": embedding}