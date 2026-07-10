from sentence_transformers import SentenceTransformer


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def create_embedding(text: str):

    if not text:
        return None


    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()