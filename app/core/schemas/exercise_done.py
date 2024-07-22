from pydantic import BaseModel
from typing import List, Optional

class ExerciseDoneBase(BaseModel):
    reps: int
    max_weight: float
    exercise_plan_id: int

class ExerciseDoneCreate(ExerciseDoneBase):
    pass

class ExerciseDoneUpdate(ExerciseDoneBase):
    workout_done_id: int
    id: int

class ExerciseDone(ExerciseDoneBase):
    workout_done_id: int
    id: int

    class Config:
        orm_mode = True

class ExerciseDoneWithName(ExerciseDoneBase):
    id: int
    exercise_name: str
    workout_done_id: int

    class Config:
        orm_mode = True
