from fastapi import APIRouter
from app.services.claim_service import create_claim
from app.models.claim import claimCreate

router = APIRouter(prefix = "/api/claims",tags=["Claims"])

@router.post("/verify")
async def verify_claims(claim:claimCreate):
    print("VERIFY ENDPOINT HIT")
    result = await create_claim(claim.text)

    return {
        "message":"Claim received",
        "data":result
    }
    