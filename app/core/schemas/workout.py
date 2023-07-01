from pydantic import BaseModel
from typing import List
from datetime import date
from core.schemas.user import User

class WorkoutBase(BaseModel):
    datetime: date
    workout_exercise_id: int
    reps: int
    max_weight: float

class WorkoutCreate(BaseModel):
    workout_exercise_id: int
    reps: int
    max_weight: float

class WorkoutUpdate(WorkoutBase):
    id: int

class Workout(WorkoutBase):
    id: int

    class Config:
        orm_mode = True

class WorkoutWithExercise(Workout):
    id: int
    exercise_name: str

    class Config:
        orm_mode = True
