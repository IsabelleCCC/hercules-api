from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.services.auth import AuthService

from app.services.user import UserService
from app.services.exceptions import NotFoundException, BadRequestException
from core.schemas.user import UserCreate, UserUpdate, User

UserRouter = APIRouter(
    prefix='/user', tags=['user']
)

@UserRouter.get("/id/{user_id}", response_model=User, dependencies=[Depends(AuthService.get_current_user)])
def get_by_id(user_id: int, user_service: UserService = Depends()):
    try:
        user = user_service.get_by_id(user_id)
        return user
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@UserRouter.get("/email/{user_email}", response_model=User, dependencies=[Depends(AuthService.get_current_user)])
def get_by_email(user_email: str, user_service: UserService = Depends()):
    try:
        user = user_service.get_by_email(user_email)
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@UserRouter.get("", response_model=List[User], dependencies=[Depends(AuthService.get_current_user)])
def list(skip: Optional[int] = 0, limit: Optional[int] = 10, user_service: UserService = Depends()):
    users = user_service.list(skip, limit)
    return users


@UserRouter.post("/signup", response_model=User)
def create(user_body: UserCreate, user_service: UserService = Depends()):
    try:
        user = user_service.create(user_body)
        return user
    except BadRequestException:
        raise HTTPException(status_code=400, detail="O usuário com este e-mail já existe.")


@UserRouter.put("", response_model=User, dependencies=[Depends(AuthService.get_current_user)])
def update(user_body: UserUpdate, user_service: UserService = Depends()):
    try:
        user = user_service.update(user_body)
        return user
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@UserRouter.delete("/{user_id}", dependencies=[Depends(AuthService.get_current_user)])
def delete(user_id: int, user_service: UserService = Depends()):
    try:
        user_service.delete(user_id)
        return {"message": "Usuário deletado."}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
