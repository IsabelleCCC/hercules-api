from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv

# Definição do repositório de login
class Auth:
    db: Session
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

    def __init__(self) -> None:
        load_dotenv()

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hashed_pass)


    def create_access_token(self, email: Union[str, Any], name: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "email": str(email), "name":str(name)}

        encoded_jwt = jwt.encode(to_encode, os.environ.get('JWT_SECRET_KEY'), os.environ.get('ALGORITHM'))
        return encoded_jwt

    def create_refresh_token(self, expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta}
        encoded_jwt = jwt.encode(to_encode, os.environ.get('JWT_REFRESH_SECRET_KEY'), os.environ.get('ALGORITHM'))
        return encoded_jwt
