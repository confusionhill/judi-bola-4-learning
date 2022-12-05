from sqlalchemy.sql import text
from model.UserModel import User, UserLogin
from fastapi import HTTPException
from services.authentication.authHandler import signJWT, sign_refresh_token
from services.authentication.auth_service import authService
from services.database.database_manager import conn

def sign_in_user(user: UserLogin):
    query = text("""SELECT * FROM users WHERE username=:uname""");
    try :
        result = conn.execute(query, {"uname": user.username})
        for row in result:
            print(result)
            if row[1] == user.username and authService.validate_password(password=user.password, hashed=row[2]):
                return {
                    "token": signJWT(row[0], user.username),
                    "refresh": sign_refresh_token(row[0], user.username)
                }
        print(result)
    except:
        print("error")
    raise HTTPException(status_code=404, detail="User Not Found")

async def register_user(user: User):
    if (len(user.username) < 5 or len(user.username) > 16):
        raise HTTPException(status_code=500, detail="username does not fulfill the requirements")
        return;
    if (len(user.password) < 8 or len(user.password) > 25):
        raise HTTPException(status_code=500, detail="Password does not fulfill the requirements")
        return;
    data = {"username": user.username, "password": authService.hash_password(user.password), "name": user.name, "coins":1000}
    statement = text("""INSERT INTO users(username,password,name, coins) VALUES(:username, :password, :name, :coins)""")
    try:
        conn.execute(statement, **data)
        for row in conn.execute(text("SELECT id from users where username=:username"),{"username": user.username}):
            return {
                "token": signJWT(row[0], user.username),
                "refresh": sign_refresh_token(row[0], user.username)
            }
        raise HTTPException(status_code=600, detail="Internal Server Error")
    except:
        raise HTTPException(status_code=505, detail="Username not unique")


async def refresh_session(token: str):
    pass

