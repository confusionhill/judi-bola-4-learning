from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql import text

from model.UserModel import UserInformation, UserTopup
from services.authentication.authBearer import JWTBearer, JWTService
from services.database.database_manager import conn

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("")
async def get_user_information(session: JWTService = Depends(JWTBearer())):
    for user in conn.execute(text("select * from users where id=:id"), {"id": session.userId}) :
        p = UserInformation()
        p.username = user[1]
        p.name = user[3]
        p.coins = user[4]
        return {
            "user-info": p
        }
    return {}

@router.post("/topup")
async def top_up_user(user: UserTopup, session: JWTService = Depends(JWTBearer())):
    try :
        query = text("update users set coins = coins +:coin where id =:id")
        conn.execute(query, {"coin": user.amount, "id": session.userId})
        return {"msg": "success"}
    except:
        raise HTTPException(status_code=505, detail="Problem Topuping your coins")

@router.get("/mybet")
async def get_my_bet(limit: int = 10, page: int = 1,session: JWTService = Depends(JWTBearer())):
    list_of_bets = []
    last_page = page * limit
    first_page = last_page - limit
    query = text("select * from users_event where user_id =:id LIMIT :l1, :l2;")
    for bets in conn.execute(query, {"id": session.userId, "l1":first_page, "l2": last_page}):
        list_of_bets.append(bets)
    return list_of_bets