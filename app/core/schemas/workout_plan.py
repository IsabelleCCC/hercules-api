from pydantic import BaseModel
from typing import List
from datetime import date
from core.schemas.user import User
from core.schemas.exercise_plan import ExercisePlanCreate, ExercisePlan

class WorkoutPlanBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    user_id: int

    class Config:
        orm_mode = True

class WorkoutPlanCreate(WorkoutPlanBase):
    exercise_plans: List[ExercisePlanCreate]

class WorkoutPlanCreated(WorkoutPlanBase):
    exercise_plans: List[ExercisePlan]
    id: int

class WorkoutPlanWithExercisePlan(WorkoutPlanBase):
    exercise_plans: List[ExercisePlan]
    id: int

    class Config:
        orm_mode = True

class WorkoutPlanUpdate(WorkoutPlanBase):
    id: int

class WorkoutPlan(WorkoutPlanBase):
    id: int

class WorkoutPlanWithUser(WorkoutPlan):
    user: User
