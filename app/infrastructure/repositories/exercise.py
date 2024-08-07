from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from core.models.exercise import Exercise as ExerciseModel
from core.schemas.exercise import ExerciseCreate, ExerciseUpdate, Exercise
from infrastructure.configs.database import get_db


class ExerciseRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, exercise_id: int) -> Exercise:
        return self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> list[Exercise]:
        return self.db.query(ExerciseModel).offset(skip).limit(limit).all()

    def create(self, exercise: ExerciseCreate) -> Exercise:
        exercise_data = ExerciseModel(name=exercise.name)
        self.db.add(exercise_data)
        self.db.commit()
        self.db.refresh(exercise_data)
        return exercise_data

    def update(self, exercise: ExerciseUpdate) -> Exercise:
        self.db.merge(exercise)
        self.db.commit()
        return exercise

    def delete(self, exercise: Exercise) -> None:
        self.db.delete(exercise)
        self.db.commit()
        self.db.flush()
