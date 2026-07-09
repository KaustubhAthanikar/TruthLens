from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class claimCreate(BaseModel):
    text: str



class SingleClaimResult(BaseModel):

    claim: str

    topic: str

    clean_text: str

    entities: list[str]

    search_query: str

    evidence_source: str

    verification: dict[str, Any]

    evidence: list[dict[str, Any]]



class Claim(BaseModel):

    original_text: str

    language: str

    total_claims: int

    claims: list[SingleClaimResult]

    created_at: datetime = Field(default_factory=datetime.now)