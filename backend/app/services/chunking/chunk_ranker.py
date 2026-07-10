from app.services.ranking.similarity_service import calculate_similarities


def rank_chunks(claim, chunks):

    if not chunks:
        return []


    scores = calculate_similarities(
        claim,
        chunks
    )


    ranked = []


    for i in range(len(chunks)):

        ranked.append(
            {
                "text": chunks[i],
                "score": round(scores[i], 3)
            }
        )


    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return ranked[:5]