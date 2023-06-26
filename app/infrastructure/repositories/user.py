from sqlalchemy.orm import Session
from fastapi import Depends
from core.models.user import User as UserModel
from core.schemas.user import UserCreate, UserUpdate, User
from typing import List
from infrastructure.configs.database import get_db

class UserRepository:
    db: Session

    def __init__(self, db: Session=Depends(get_db)) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()


    def get_by_email(self, email: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.email == email).first()


    def list(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return self.db.query(UserModel).offset(skip).limit(limit).all()


    def create(self, user: UserCreate) -> UserModel:
        db_user = UserModel(email=user.email, name=user.name, gender=user.gender, birth_date=user.birth_date)
        db_user.password = user.password
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    def update(self, user: UserUpdate) -> UserModel:
        self.db.merge(user)
        self.db.commit()
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()
