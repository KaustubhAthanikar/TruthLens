def generate_trust_report(claim_result):


    verification = claim_result["verification"]


    verdict = verification.get("verdict","UNCERTAIN")


    confidence = verification.get("confidence", 0)


    if verdict == "SUPPORTS":

        label = "Mostly True"



    elif verdict == "REFUTES":

        label = "Likely False"



    else:

        label = "Needs More Context"



    sources = []


    for source in claim_result.get("sources",[]):

        sources.append(
            {
                "title":source.get("title"),
                "url":source.get("url")
            }

        )



    return {

        "display_verdict":label,

        "confidence":confidence,

        "claim":claim_result["claim"],

        "summary":verification.get("reason"),

        "evidence":verification.get("evidence_quote"),

        "sources":sources

    }