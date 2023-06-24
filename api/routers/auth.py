from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.services.auth import AuthService
from app.services.exceptions import NotFoundException, UnauthorizedException
from app.view_models.auth import UserLogin, UserToken, SystemUser

AuthRouter = APIRouter(
    prefix='/auth', tags=['auth']
)


@AuthRouter.post("/login", response_model=UserToken)
def login(login_body: UserLogin, auth_service: AuthService = Depends()):
    try:
        response = auth_service.login(login_body)
        return response
    except NotFoundException:
        raise HTTPException(status_code=404, detail="E-mail incorreto.")
    except UnauthorizedException:
        raise HTTPException(status_code=404, detail="Senha incorreta.")
