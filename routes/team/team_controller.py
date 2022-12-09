from fastapi import APIRouter, HTTPException

from model.TeamModel import TeamPlayerModel
from services.database.database_manager import conn
from sqlalchemy.sql import text
import requests

router = APIRouter(prefix="/team", tags=["Team"])

@router.get("")
async def get_available_teams(page: int = 1, limit: int = 10):
    last_page = limit*page
    first_page = last_page - limit
    result = conn.execute(text("SELECT * FROM Teams LIMIT :f1,:l1"), {"f1": first_page, "l1": last_page} )
    teams = []
    for team in result:
        teams.append({"id": team[0], "name":team[1]})
    return {
        "teams": teams
    }

@router.get("/players")
def get_team_players(team_id: int = 10):
    query = text("SELECT teamName FROM Teams WHERE id=:id")
    for team in conn.execute(query, {"id": team_id}):
        squad = team["teamName"]
        url = f"http://128.199.149.182:8028/player/{squad}"
        body = {}
        headers = {}
        response = requests.get(url, json=body, headers=headers)
        return response.json()
    raise HTTPException(status_code=404, detail="Team is not registered in the World Cup 2022")