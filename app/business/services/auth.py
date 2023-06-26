from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union, Any
from datetime import datetime
from jose import jwt
from pydantic import ValidationError
import os
from dotenv import load_dotenv

from api.utils.auth import Auth
from infrastructure.repositories.user import UserRepository
from business.view_models.auth import UserLogin, UserToken
from business.services.exceptions import NotFoundException, UnauthorizedException
from fastapi.security import OAuth2PasswordBearer
from business.view_models.auth import TokenPayload, SystemUser

class AuthService:
    auth: Auth
    userRepository: UserRepository

    reuseable_oauth = OAuth2PasswordBearer(
        tokenUrl="/auth/login",
    )

    def __init__(self, authRepository: Auth = Depends(), userRepository: UserRepository = Depends()) -> None:
        self.auth = authRepository
        self.userRepository = userRepository

    def login(self, login_body: OAuth2PasswordRequestForm = Depends()) -> UserToken:
        user = self.userRepository.get_by_email(email=login_body.email)

        if not user:
            raise NotFoundException()

        hashed_pass = user.password
        if not self.auth.verify_password(login_body.password, hashed_pass):
            raise UnauthorizedException()

        return {
            "access_token": self.auth.create_access_token(user.email, user.name),
            "refresh_token": self.auth.create_refresh_token(),
        }

    def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
        load_dotenv()
        try:
            payload = jwt.decode(
                token, os.environ.get('JWT_SECRET_KEY'), algorithms=[os.environ.get('ALGORITHM')]
            )
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except(jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if token_data.email is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        return token_data
