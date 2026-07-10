from fastapi import FastAPI
from pydantic import BaseModel

from embedding.embedding_service import (
    create_embedding,
    create_embeddings
)


app = FastAPI()



class SingleEmbedRequest(BaseModel):

    text: str



class BatchEmbedRequest(BaseModel):

    texts: list[str]




@app.get("/")
def home():

    return {
        "service": "TruthLens Embedding Service running"
    }



@app.head("/")
def health():

    return




@app.post("/embed")
def embed(req: SingleEmbedRequest):

    embedding = create_embedding(req.text)

    return {
        "embedding": embedding
    }




@app.post("/embed/batch")
def embed_batch(req: BatchEmbedRequest):

    embeddings = create_embeddings(req.texts)

    return {
        "embeddings": embeddings
    }