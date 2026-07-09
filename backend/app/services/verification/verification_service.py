from app.services.verification.verifier_chain import verification_chain



def verify_claim(claim, evidence):

    evidence_text = ""


    for item in evidence:


        chunks = item.get("top_chunks",[])


        for chunk in chunks:


            evidence_text += (chunk.get("text", "")+"\n\n" )



    result = verification_chain.invoke(
        {
            "claim": claim,

            "evidence": evidence_text
        }
    )


    return result