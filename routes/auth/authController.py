from fastapi import APIRouter
from model.UserModel import User
from services.authentication.authHandler import signJWT

router = APIRouter()

@router.post("/register")
async def create_user(user: User):
    return signJWT(user.email)

@router.post("/login")
async def sign_in_user(user: User):
    return signJWT(user.email)