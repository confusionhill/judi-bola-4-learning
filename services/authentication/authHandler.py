
import time
from typing import Dict
from fastapi import HTTPException
from dotenv import load_dotenv, dotenv_values
import jwt

load_dotenv()
config = dotenv_values(".env")
JWT_SECRET = config["JWT_SECRET"]
JWT_ALGORITHM = config["JWT_ALGORITHM"]
REFRESH_ALGORITHM = config["REFRESH_ALGORITHM"]
REFRESH_SECRET = config["REFRESH_SECRET"]


def token_response(token: str):
    return token

def signJWT(user_id: int, username: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "username": username,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        raise HTTPException(status_code=503, detail="Failed to authenticate")

def sign_refresh_token(user_id: int, username: str):
    payload = {
        "user_id": user_id,
        "username": username,
        "expires": time.time()*2
    }
    token = jwt.encode(payload, REFRESH_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_refresh_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, REFRESH_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        raise HTTPException(status_code=503, detail="Failed to authenticate")