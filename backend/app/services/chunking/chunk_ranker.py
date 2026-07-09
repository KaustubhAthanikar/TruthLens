from app.services.chunking.chunk_service import create_chunks
from app.services.ranking.similarity_service import calculate_similarity

def rank_chunks(claim,evidence):
    content = evidence.get("content","")
    chunks = create_chunks(content)

    ranked_chunks = []

    for chunk in chunks:
        score = calculate_similarity(claim,chunk)
        ranked_chunks.append({
            "text":chunk,
            "similarity_score":round(score,3)
        })
    ranked_chunks.sort(key=lambda x:x["similarity_score"],reverse=True)
    filtered = []


    for chunk in ranked_chunks:

        if chunk["similarity_score"]>= 0.35 and len(chunk["text"]) > 100 :

            filtered.append(chunk)


    return filtered[:5]