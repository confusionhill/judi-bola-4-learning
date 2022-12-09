from model.JudiModel import EventModel, BetModel
from services.database.database_manager import conn
from sqlalchemy.sql import text
from fastapi import HTTPException

def get_specific_event(id:int):
    query = text("""
        select e.id as id, e.name as name, e.description as description, 
        e.start_campaign as start_campaign, e.end_campaign as end_campaign, 
        e.home_team_id as home_team_id, t1.teamName as home_team_name, 
        t2.id as away_team_id, t2.teamName as away_team_name 
        from events as e 
        inner join Teams as t1 on e.home_team_id = t1.id 
        inner join Teams as t2  on e.away_team_id = t2.id
        where e.id = :id
        ;""")
    for row in conn.execute(query, {"id": id}):
        return EventModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    raise HTTPException(status_code=404, detail="Event not found")

def get_all_events(limit: int, page: int):
    query = text("""
    select e.id as id, e.name as name, e.description as description, 
    e.start_campaign as start_campaign, e.end_campaign as end_campaign, 
    e.home_team_id as home_team_id, t1.teamName as home_team_name, 
    t2.id as away_team_id, t2.teamName as away_team_name 
    from events as e 
    inner join Teams as t1 on e.home_team_id = t1.id 
    inner join Teams as t2  on e.away_team_id = t2.id
    LIMIT :l1,:l2
    ;""")
    models = []
    last_page = page * limit
    first_page = last_page - limit
    for row in conn.execute(query , {"l1": first_page, "l2": last_page }):
        print(row)
        model = EventModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        models.append(model)
    return {"data": models} #models

def place_bet(bet: BetModel, userId):
    query = text("""
    INSERT INTO users_event(bet, event_id, user_id, team_id ) VALUES (:bet, :event_id, :user_id, :team_id)
    """)
    try:
        for coin in conn.execute(text("select coins from users where id =:id"), {"id": userId}):
            coin = int(coin[0])
            if coin < bet.amount:
                return {
                    "error": "You're low on coin"
                }
            newC = coin - bet.amount
            conn.execute(text("update users set coins =:coin where id =:id"), {"coin": newC, "id": userId})
        conn.execute(query, {
            "bet": bet.amount,
            "event_id": bet.event_id,
            "user_id": userId,
            "team_id": bet.team_id
        })
        return {"msg": "Success"}
    except :
        raise HTTPException(status_code=505, detail="Problem Adding your bet")