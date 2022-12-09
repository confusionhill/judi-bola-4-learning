from typing import Optional

from fastapi import APIRouter, Header, FastAPI, Depends
from model.UserModel import User, UserLogin
from routes.auth.auth_service import register_user, sign_in_user, refresh_session
from services.authentication.authBearer import JWTService, JWTBearer

router = APIRouter(
    tags=["Authentication"]
)

app = FastAPI()

@router.post("/register")
async def create_user(user: User):
    return await register_user(user);

@router.post("/login")
async def sign_in(user: UserLogin):
    return sign_in_user(user)

@router.post("/refresh")
async def refresh_token(refresh: Optional[str] = Header(None)):
    result = await refresh_session(refresh)
    return result

@app.post("/validate")
async def validate_jwt_extern(session: JWTService = Depends(JWTBearer())):
    return session