from infrastructure.repositories.user import UserRepository
from core.schemas.user import UserCreate, UserUpdate
from core.models.user import User
from business.services.exceptions import NotFoundException, BadRequestException
from fastapi import Depends
from typing import List, Optional
from api.utils.auth import Auth


class UserService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends(), auth: Auth = Depends()) -> None:
        self.userRepository = userRepository
        self.auth = auth

    def create(self, user_body: UserCreate) -> User:
        user = self.userRepository.get_by_email(email=user_body.email)
        if user is not None:
            raise BadRequestException()

        hashed_password = self.auth.get_hashed_password(user_body.password)

        return self.userRepository.create(User(name=user_body.name,
                                               gender=user_body.gender,
                                               birth_date=user_body.birth_date,
                                               email=user_body.email,
                                               password=hashed_password))

    def get_by_id(self, user_id: int) -> User:
        user = self.userRepository.get_by_id(user_id)
        if not user:
            raise NotFoundException()
        return user

    def get_by_email(self, user_email: str) -> User:
        user = self.userRepository.get_by_email(user_email)
        if not user:
            raise NotFoundException()
        return user

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[User]:
        return self.userRepository.list(skip, limit)

    def update(self, user_body: UserUpdate) -> User:
        user = self.userRepository.get_by_id(user_body.id)
        if not user:
            raise NotFoundException()

        return self.userRepository.update(User(id=user_body.id,
                                               name=user_body.name,
                                               gender=user_body.gender,
                                               birth_date=user_body.birth_date,
                                               email=user_body.email,
                                               password=user_body.email))

    def delete(self, user_id: int):
        user = self.userRepository.get_by_id(user_id)
        if not user:
            raise NotFoundException()
        return self.userRepository.delete(user)
