from sentence_transformers import SentenceTransformer
import os


os.environ["TOKENIZERS_PARALLELISM"] = "false"


model = None


def get_model():

    global model

    if model is None:

        print("Loading embedding model...")

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

        print("Embedding model loaded")

    return model



def create_embedding(text: str):

    if not text:
        return None


    model = get_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()



def create_embeddings(texts: list[str]):

    if not texts:
        return []


    model = get_model()

    embeddings = model.encode(
        texts,
        batch_size=32,
        normalize_embeddings=True
    )

    return embeddings.tolist()