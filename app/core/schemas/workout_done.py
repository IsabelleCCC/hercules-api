from pydantic import BaseModel
from typing import List
from datetime import datetime
from core.schemas.user import User
from core.schemas.exercise_done import ExerciseDoneCreate, ExerciseDone

class WorkoutDoneBase(BaseModel):
    datetime: datetime
    duration: float
    workout_plan_id: int

class WorkoutDoneCreate(WorkoutDoneBase):
    exercises_done: List[ExerciseDoneCreate]
    pass

class WorkoutDoneUpdate(WorkoutDoneBase):
    id: int

class WorkoutDone(WorkoutDoneBase):
    id: int
    exercises_done: List[ExerciseDone]

    class Config:
        orm_mode = True

class WorkoutDoneWithName(WorkoutDoneBase):
    id: int
    workout_name: str

    class Config:
        orm_mode = True
