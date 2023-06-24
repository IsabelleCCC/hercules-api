from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    gender: str
    birth_date: date

class UserUpdate(UserBase):
    id: int
    password: str
    gender: str
    birth_date: date

class User(UserBase):
    id: int
    gender: str
    birth_date: date
    password: str
    class Config:
        orm_mode = True
