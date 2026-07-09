import numpy as np
from app.services.ranking.embedding_service import create_embedding

def calculate_similarity(claim:str,evidence:str):
    claim_vector = create_embedding(claim)
    evidence_vector = create_embedding(evidence)
    if claim_vector is None or evidence_vector is None:
        return 0
    score = np.dot(claim_vector,evidence_vector)

    return float(score)