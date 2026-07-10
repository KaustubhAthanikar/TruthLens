import numpy as np

from app.services.ai_client import create_embeddings


def calculate_similarities(claim: str, texts: list):

    if not texts:
        return []


    vectors = create_embeddings(
        [claim] + texts
    )


    claim_vector = vectors[0]


    scores = []


    for i in range(1, len(vectors)):

        score = np.dot(
            claim_vector,
            vectors[i]
        )

        scores.append(float(score))


    return scores