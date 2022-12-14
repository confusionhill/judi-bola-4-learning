from fastapi import APIRouter, Depends

from model.JudiModel import BetModel
from routes.judi.judi_service import get_all_events, place_bet, get_specific_event
from services.authentication.authBearer import JWTService, JWTBearer

router = APIRouter(
    prefix="/judi",
    tags=["Judi"]
)

@router.post("/bet")
def place_user_bet(bet: BetModel, session: JWTService = Depends(JWTBearer())):
    return place_bet(bet, session.userId)

@router.get("/events")
def get_available_events(limit: int = 10, page: int = 1):
    return get_all_events(limit=limit, page=page)

@router.get("/events/{id}")
async def get_event_info(id: int):
    return get_specific_event(id=id)
