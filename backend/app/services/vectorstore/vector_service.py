import uuid

from app.services.vectorstore.pinecone_client import get_index

from app.services.ranking.embedding_service import create_embedding

from app.services.ranking.credibility_service import calculate_credibility


index = get_index()

def store_evidence_chunks(chunks, metadata):

    vectors = []

    for chunk in chunks:

        text = chunk.get("text")

        if not text:
            continue

        embedding = create_embedding(text)

        vectors.append(
            {
                "id": str(uuid.uuid4()),

                "values": embedding.tolist(),

                "metadata": {

                    "text": text,

                    "url": str(metadata.get("url","")),

                    "source": str(metadata.get("source","")),

                    "title": str(metadata.get("title",""))

                }

            }

        )


    if vectors:

        index.upsert(
            vectors=vectors
        )



def search_cached_evidence(claim, threshold=0.55):

    embedding = create_embedding(claim)

    result = index.query(

        vector=embedding.tolist(),

        top_k=10,

        include_metadata=True
    )

    evidence = []

    for match in result.matches:

        if match.score >= threshold:

            source = match.metadata.get("source","")


            credibility = calculate_credibility(source)

            final_score = (match.score * 0.5 + credibility * 0.5)

            evidence.append(
                {
                    "url":match.metadata.get("url"),

                    "source":source,


                    "title":match.metadata.get("title"),

                    "top_chunks": [
                        {
                            "text":match.metadata.get("text",""),

                            "similarity_score":round(match.score,3)
                        }

                    ],


                    "similarity_score":round(match.score,3),

                    "credibility_score":credibility,

                    "final_score":round(final_score,3)
                }

            )



    evidence.sort(

        key=lambda x: x["final_score"],

        reverse=True

    )



    return evidence[:5]