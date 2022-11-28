from datetime import datetime
from pydantic.main import BaseModel


class BetModel(BaseModel):
    event_id: int
    team_id: int
    amount: int

class EventModel:
    def __init__(self, id, name, desc, start_campaign, end_campaign, home_team_id, home_team_name, away_team_id, away_team_name):
        self.id = id
        self.name = name
        self.desc = desc
        self.start_campaign = start_campaign
        self.end_campaign = end_campaign
        self.home_team_id = home_team_id
        self.home_team_name = home_team_name
        self.away_team_id = away_team_id
        self.away_team_name = away_team_name
    id: int
    name: str
    desc: str
    # start_campaign: datetime
    # end_campaign: datetime
    home_team_id: int
    home_team_name: str
    away_team_id: int
    away_team_name: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "start-campaign": self.start_campaign,
            "end-campaign": self.end_campaign,
            "home-team-id": self.home_team_id,
            "home-team-name": self.home_team_name,
            "away-team-id": self.away_team_id,
            "away-team-name": self.away_team_name
        }
