import numpy as np

from app.services.ai_client import create_embeddings


def calculate_similarity(claim: str, evidence: str):

    vectors = create_embeddings(
        [
            claim,
            evidence
        ]
    )


    if not vectors:
        return 0


    claim_vector = vectors[0]

    evidence_vector = vectors[1]


    score = np.dot(
        claim_vector,
        evidence_vector
    )


    return float(score)