from datetime import datetime

from app.database.mongodb import get_database

from app.services.intelligence.intelligence_service import analyze_claim

from app.services.nlp.cleaner import clean_text
from app.services.nlp.entity_extractor import extract_entities
from app.services.nlp.query_generator import generate_query

from app.services.retrieval.evidence_service import retrieve_evidence

from app.services.ranking.ranking_service import rank_evidence

from app.services.verification.verification_service import verify_claim

from app.services.vectorstore.vector_service import (search_cached_evidence,store_evidence_chunks)
from app.services.reports.report_service import generate_trust_report


async def create_claim(text: str):

    db = get_database()

    analysis = analyze_claim(text)

    final_results = []

    for item in analysis["claims"]:
        claim_text = item["claim"]
        cleaned_text = clean_text(claim_text)
        entities = extract_entities(cleaned_text)
        query = generate_query(
            cleaned_text,
            entities
        )
        cached_evidence = search_cached_evidence(
            claim_text
        )

        if cached_evidence:
            final_evidence = cached_evidence
            evidence_source = "VECTOR_CACHE"

        else:

            evidence = retrieve_evidence(query)  

            ranked_evidence = rank_evidence(
                claim_text,
                evidence
            )


            

            final_evidence = [item for item in ranked_evidence if item.get("top_chunks")][:5]

            

            for evidence_item in final_evidence:
                store_evidence_chunks(
                    evidence_item["top_chunks"],
                    {
                        "url": evidence_item["url"],
                        "source": evidence_item["source"],
                        "title": evidence_item["title"]
                    }
                )


            evidence_source = "WEB"



        if not final_evidence:
            verification = {
                "verdict": "UNABLE_TO_VERIFY",
                "confidence": 0,
                "reason": "No relevant evidence could be retrieved."
            }
        else:
            verification = verify_claim(claim_text, final_evidence)



        claim_result = {
            "claim": claim_text,
            "topic": item["topic"],
            "clean_text": cleaned_text,
            "entities": entities,
            "search_query": query,
            "evidence_source": evidence_source,
            "verification": verification,
            "evidence": final_evidence,
            "sources":[
                {
                    "title":x.get("title"),
                    "url":x.get("url"),
                    "source":x.get("source")
                }
                 for x in final_evidence
            ]
        }

        claim_result["trust_report"] = generate_trust_report(claim_result)



        final_results.append(claim_result)

    document = {

        "original_text":text,

        "processed_text":analysis["translated_text"],

        "language":analysis["original_language"],

        "total_claims":len(final_results),

        "claims":final_results,

        "created_at":datetime.now()

    }



    result = await db.claim.insert_one(
        document
    )


    document["_id"] = str(
        result.inserted_id
    )


    return document