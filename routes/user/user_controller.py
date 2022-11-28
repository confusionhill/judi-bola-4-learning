from fastapi import APIRouter, Depends
from sqlalchemy.sql import text

from model.UserModel import UserInformation, UserTopup
from services.authentication.authBearer import JWTBearer
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

@router.post("/topup", dependencies=[Depends(JWTBearer())])
async def toptup(user: UserTopup):
    return {}