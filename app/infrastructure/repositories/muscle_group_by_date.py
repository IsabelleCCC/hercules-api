from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from core.models.muscle_group_by_date import MuscleGroupByDate as MuscleGroupByDateModel
from core.schemas.muscle_group_by_date import MuscleGroupByDate
from infrastructure.configs.database import get_db


class MuscleGroupByDateRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> list[MuscleGroupByDate]:
        return self.db.query(MuscleGroupByDateModel).filter(MuscleGroupByDateModel.user_id == user_id).offset(skip).limit(limit).all()

