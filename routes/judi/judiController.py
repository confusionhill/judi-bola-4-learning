from fastapi import APIRouter, Depends

from model.JudiModel import BetModel
from routes.judi.judi_service import get_all_events, place_bet
from services.authentication.authBearer import JWTService, JWTBearer

router = APIRouter(
    prefix="/judi",
    tags=["Judi"]
)

@router.post("/bet")
def place_user_bet(bet: BetModel, session: JWTService = Depends(JWTBearer())):
    return place_bet(bet, session.userId)

@router.get("/events")
def get_available_events():
    return get_all_events()

@router.get("/events/{id}")
async def get_event_info():
    return {}
