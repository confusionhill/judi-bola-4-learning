from pydantic import BaseModel

class User(BaseModel):
    username: str
    name:str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInformation:
    username: str
    name: str
    coins: int

class UserTopup(BaseModel):
    amount: int