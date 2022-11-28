from model.JudiModel import EventModel
from services.database.database_manager import conn
from sqlalchemy.sql import text

def get_all_events():
    query = text("""
    select e.id as id, e.name as name, e.description as description, 
    e.start_campaign as start_campaign, e.end_campaign as end_campaign, 
    e.home_team_id as home_team_id, t1.teamName as home_team_name, 
    t2.id as away_team_id, t2.teamName as away_team_name 
    from events as e 
    inner join Teams as t1 on e.home_team_id = t1.id 
    inner join Teams as t2  on e.away_team_id = t2.id;""")
    models = []
    for row in conn.execute(query):
        print(row)
        model = EventModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        models.append(model)
    return {"data": models} #models