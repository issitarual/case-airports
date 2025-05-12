from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health Check"])
async def health():
    return {"status": "ok", "message": "API is running."}
