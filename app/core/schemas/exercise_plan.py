from pydantic import BaseModel
from typing import List, Optional

class ExercisePlanBase(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    combination: Optional[int]


class ExercisePlanCreate(ExercisePlanBase):
    pass

class ExercisePlanUpdate(ExercisePlanBase):
    workout_plan_id: int
    id: int


class ExercisePlan(ExercisePlanBase):
    id: int
    workout_plan_id: int
    exercise_name: str

    class Config:
        orm_mode = True

class ExercisePlanWithName(ExercisePlanBase):
    id: int
    exercise_name: str
    workout_plan_id: int

    class Config:
        orm_mode = True
