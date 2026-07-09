from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import JsonOutputParser

from app.config.settings import settings



llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    google_api_key=settings.GEMINI_API_KEY

)


parser = JsonOutputParser()



prompt = ChatPromptTemplate.from_template(
"""

You are a fake news verification system.

Verify the claim ONLY using the given evidence.

Do not use outside knowledge.


Claim:

{claim}



Evidence:

{evidence}



Return ONLY valid JSON in this format:


{{
    "verdict":"SUPPORTS | REFUTES | UNCERTAIN",

    "confidence":number between 0 and 100,

    "evidence_quote":"exact quote from evidence",

    "reason":"short explanation"
}}


Rules:

- Evidence quote must exist in provided evidence.
- If evidence is insufficient return UNCERTAIN.

"""
)



verification_chain = prompt|llm|parser