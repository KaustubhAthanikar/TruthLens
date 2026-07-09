from app.services.ranking.similarity_service import calculate_similarity
from app.services.ranking.credibility_service import calculate_credibility
from app.services.ranking.freshness_service import calculate_freshness
from app.services.chunking.chunk_ranker import rank_chunks

def rank_evidence(claim,evidences):
    ranked=[]
    for evidence in evidences:
        content = evidence.get("content","")
        semantic_score = calculate_similarity(claim,content)
        best_chunks = rank_chunks(claim,evidence)
        credibility_score = calculate_credibility(evidence.get("url"))
        freshness_score = calculate_freshness(evidence.get("retrieved_at"))

        final_score = semantic_score*0.45 + credibility_score*0.45 + freshness_score*0.1
        evidence["similarity_score"]=round(semantic_score,3)

        evidence["credibility_score"]=round(credibility_score,3)

        evidence["freshness_score"]=round(freshness_score,3)

        evidence["final_score"]=round(final_score,3)
        evidence["top_chunks"] = best_chunks

        ranked.append(evidence)
    ranked.sort(key=lambda x:x["final_score"],reverse=True)
    return ranked