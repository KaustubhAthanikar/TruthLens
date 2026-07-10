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
You are a factual claim verification system.

Verify the claim ONLY using the given evidence.

Do not use outside knowledge.

Claim:{claim}

Evidence:{evidence}

Return ONLY valid JSON in this format:
{{
    "verdict":"SUPPORTS | REFUTES | UNCERTAIN",

    "confidence":number between 0 and 100,

    "evidence_quote":"exact quote from evidence",

    "reason":"short explanation"
}}

Verdict rules:

SUPPORTS:
Use only when the evidence directly proves the claim.

Confidence:
90-100:
The evidence clearly proves the claim with strong factual support.

70-90:
The evidence supports the claim but with limited sources.

50-70:
The evidence partially supports the claim.


REFUTES:
Use only when the evidence directly contradicts the claim.

Confidence:
90-100:
The evidence clearly disproves the claim.

70-90:
Strong contradiction exists.

50-70:
Partial contradiction exists.


UNCERTAIN:
Use when:
- Evidence is related but does not prove the claim.
- Evidence is missing important facts.
- The claim is subjective or opinion-based.
- The claim cannot be objectively verified.

UNCERTAIN confidence:
0-30:
Almost no relevant evidence.

30-60:
Some related evidence exists, but the claim cannot be proven.

NEVER return confidence above 60 for UNCERTAIN.

Important:
Words like:"best","greatest","top","number one","most beautiful","worst" usually indicate subjective claims.

Popularity, awards, followers, views, or fame do NOT prove such claims.


Evidence quote rules:
- Quote must exist exactly inside provided evidence.
- Do not create quotes.


Return JSON only.

"""
)



verification_chain = prompt|llm|parser