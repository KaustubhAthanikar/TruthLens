from app.services.retrieval.evidence_service import retrieve_evidence


query = "NASA aliens 2026"


result = retrieve_evidence(
    query
)


for r in result:

    print(
        r["title"]
    )

    print(
        r["url"]
    )

    print("----------------")