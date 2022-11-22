from pydantic import BaseModel

class User(BaseModel):
    username: str
    name:str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str