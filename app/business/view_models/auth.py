from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    email: str

class UserLogin(UserBase):
    email: str
    password: str

class User(UserBase):
    id: int
    name: str
    gender: str
    birth_date: date

    class Config:
        orm_mode = True

class SystemUser(UserBase):
    id: int

class UserToken(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    exp: int = None
    email: str = None
    name: str = None
