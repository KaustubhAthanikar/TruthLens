from app.services.ranking.similarity_service import calculate_similarities
from app.services.ranking.credibility_service import calculate_credibility
from app.services.ranking.freshness_service import calculate_freshness
from app.services.chunking.chunk_ranker import rank_chunks


def rank_evidence(claim, evidences):

    if not evidences:
        return []


    contents = []


    for evidence in evidences:

        contents.append(
            evidence.get("content", "")
        )


    semantic_scores = calculate_similarities(
        claim,
        contents
    )


    ranked = []


    for i in range(len(evidences)):

        evidence = evidences[i]


        semantic_score = semantic_scores[i]


        credibility_score = calculate_credibility(
            evidence.get("url")
        )


        freshness_score = calculate_freshness(
            evidence.get("retrieved_at")
        )


        final_score = (
            semantic_score * 0.45
            + credibility_score * 0.45
            + freshness_score * 0.1
        )


        evidence["similarity_score"] = round(
            semantic_score,
            3
        )


        evidence["credibility_score"] = round(
            credibility_score,
            3
        )


        evidence["freshness_score"] = round(
            freshness_score,
            3
        )


        evidence["final_score"] = round(
            final_score,
            3
        )

        print(
            evidence["title"],
            "Chunks:",
            len(evidence.get("chunks", []))
        )

        evidence["top_chunks"] = rank_chunks(
            claim,
            evidence.get("chunks", [])
)


        ranked.append(evidence)



    ranked.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    return ranked