from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from fastapi.security import OAuth2PasswordRequestForm

from business.services.auth import AuthService
from business.services.exceptions import NotFoundException, UnauthorizedException
from business.view_models.auth import UserLogin, UserToken, SystemUser

AuthRouter = APIRouter(
    prefix='/auth', tags=['auth']
)

auth_service = AuthService()

@AuthRouter.post("/login", response_model=UserToken)
def login(login_body: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    try:
        response = auth_service.login(login_body)
        return response
    except NotFoundException:
        raise HTTPException(status_code=404, detail="E-mail incorreto.")
    except UnauthorizedException:
        raise HTTPException(status_code=404, detail="Senha incorreta.")
