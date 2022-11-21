from fastapi import APIRouter

router = APIRouter(prefix="/judi")

@router.post("/bet")
async def place_bet():
    return {}

@router.get("/events")
async def getAvailableEvents():
    return {}
