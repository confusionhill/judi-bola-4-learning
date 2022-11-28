from fastapi import APIRouter, Depends
from services.authentication.authBearer import JWTBearer, JWTService

from model.predictionModel import TeamPlaying
from services.predictionService import predict_winner

router = APIRouter(prefix="/predict")

@router.post("/")
def get_prediction(playing: TeamPlaying, Authorize: JWTService = Depends(JWTBearer())):
    print("hasil : ", Authorize.userId)
    return predict_winner(playing)
