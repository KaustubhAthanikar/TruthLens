import numpy as np

from app.services.ai_client import create_embeddings



def calculate_similarities(claim: str, evidences: list):


    if not evidences:
        return []


    texts = [claim] + evidences


    vectors = create_embeddings(texts)


    claim_vector = vectors[0]


    scores = []


    for i in range(1, len(vectors)):

        score = np.dot(
            claim_vector,
            vectors[i]
        )

        scores.append(
            float(score)
        )


    return scores