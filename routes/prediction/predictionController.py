from fastapi import APIRouter, Depends
from services.authentication.authBearer import JWTBearer

from model.predictionModel import TeamPlaying
from services.predictionService import predict_winner

router = APIRouter(prefix="/predict")

@router.post("/",dependencies=[Depends(JWTBearer())])
def get_prediction(playing: TeamPlaying):
    return predict_winner(playing)
