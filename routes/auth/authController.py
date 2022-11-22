from fastapi import APIRouter, HTTPException
from model.UserModel import User, UserLogin
from services.authentication.authHandler import signJWT
from services.authentication.auth_service import authService
from services.database.database_manager import conn
from sqlalchemy.sql import text
router = APIRouter()

@router.post("/register")
async def create_user(user: User):
    if (len(user.username) < 5 or len(user.username) > 16):
        raise HTTPException(status_code=500, detail="username does not fulfill the requirement")
    if (len(user.password) < 8 or len(user.password) > 25):
        raise HTTPException(status_code=500, detail="Requirement not fulfilled")
    data = {"username": user.username, "password": authService.hash_password(user.password), "name": user.name}
    statement = text("""INSERT INTO users(username,password,name) VALUES(:username, :password, :name)""")
    try:
        conn.execute(statement, **data)
        return signJWT(user.username)
    except:
        raise HTTPException(status_code=505, detail="Username not unique")

@router.post("/login")
async def sign_in_user(user: UserLogin):
    query = text("""SELECT * FROM users where username=:val""");
    result = conn.execute(query, {'val': user.username })
    for row in result:
        if row[1] == user.username and authService.validate_password(password=user.password,hashed=row[2]):
            return signJWT(user.username)
    raise HTTPException(status_code=404, detail="User Not Found")