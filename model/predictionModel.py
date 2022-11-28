from pydantic import BaseModel

class TeamPlaying():
    def __init__(self, teamA, teamB):
        self.teamA = teamA
        self.teamB = teamB
    teamA: str
    teamB: str

class TeamsGetter(BaseModel):
    team_home_id: int
    team_away_id: int

class PredictionModel(BaseModel):
    teamA: str
    teamB: str
    result: str
    teamAProb: float
    teamBProb: float
    drawProb: float