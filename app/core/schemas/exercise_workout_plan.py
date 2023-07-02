from pydantic import BaseModel
from typing import List, Optional

class ExerciseWorkoutPlanBase(BaseModel):
    exercise_id: int
    workout_plan_id: int
    sets: int
    reps: int
    combination: Optional[int]


class ExerciseWorkoutPlanCreate(ExerciseWorkoutPlanBase):
    pass


class ExerciseWorkoutPlanUpdate(ExerciseWorkoutPlanBase):
    id: int


class ExerciseWorkoutPlan(ExerciseWorkoutPlanBase):
    id: int

    class Config:
        orm_mode = True

class ExerciseWorkoutPlanWithName(ExerciseWorkoutPlanBase):
    id: int
    exercise_name: str
    workout_id: int
    workout_reps: Optional[int]
    workout_max_weight: Optional[float]

    class Config:
        orm_mode = True
