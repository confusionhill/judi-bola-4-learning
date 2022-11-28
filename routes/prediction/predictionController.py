from fastapi import APIRouter, Depends
from services.authentication.authBearer import JWTBearer, JWTService

from model.predictionModel import TeamPlaying, TeamsGetter
from services.database.database_manager import conn
from services.predictionService import predict_winner
from sqlalchemy import text

router = APIRouter(
    prefix="/predict",
    tags=["Machine Learning"]
)

@router.post("/")
def get_prediction(playing: TeamsGetter, Authorize: JWTService = Depends(JWTBearer())):
    teams = ["",""]
    for team in conn.execute(text("select * from Teams where id=:home or id =:away"),  {"home": playing.team_home_id , "away": playing.team_away_id}):
        if team[0] == playing.team_home_id:
            teams[0] = team[1]
        else:
            teams[1] = team[1]
    return predict_winner(TeamPlaying(teams[0], teams[1]))
