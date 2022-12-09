from typing import Optional

from fastapi import APIRouter, Header
from model.UserModel import User, UserLogin
from routes.auth.auth_service import register_user, sign_in_user, refresh_session

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
async def create_user(user: User):
    return await register_user(user);

@router.post("/login")
async def sign_in(user: UserLogin):
    return sign_in_user(user)

@router.post("/refresh")
async def refresh_token(refresh: Optional[str] = Header(None)):
    return refresh_session(refresh)