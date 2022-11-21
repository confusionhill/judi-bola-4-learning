from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

class TeamPlaying(BaseModel):
    teamA: str
    teamB: str

class PredictionModel(BaseModel):
    teamA: str
    teamB: str
    result: str
    teamAProb: float
    teamBProb: float
    drawProb: float