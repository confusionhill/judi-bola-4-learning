from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql import text

from model.UserModel import UserInformation, UserTopup
from services.authentication.authBearer import JWTBearer, JWTService
from services.database.database_manager import conn

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/{id",dependencies=[Depends(JWTBearer())])
async def getUserInformation(id: int):
    for user in conn.execute(text("select * from users where id=:id"), {"id":id}) :
        p = UserInformation()
        p.username = user[1]
        p.name = user[3]
        p.coins = user[4]
        return {
            "user-info": p
        }
    return {}

@router.post("/topup")
async def toptup(user: UserTopup, session: JWTService = Depends(JWTBearer())):
    try :
        query = text("update users set coins = coins +:coin where id =:id")
        conn.execute(query, {"coin": user.amount, "id": session.userId})
        return {"msg": "success"}
    except:
        raise HTTPException(status_code=505, detail="Problem Topuping your coins")
@router.get("/mybet")
async def get_my_bet(session: JWTService = Depends(JWTBearer())):
    list_of_bets = []
    query = text("select * from users_event where user_id =:id")
    for bets in conn.execute(query, {"id": session.userId}):
        list_of_bets.append(bets)
    return list_of_bets