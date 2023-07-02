from pydantic import BaseModel
from typing import List
from datetime import date
from core.schemas.user import User
from core.schemas.exercise_workout_plan import ExerciseWorkoutPlanCreate, ExerciseWorkoutPlan

class WorkoutPlanBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    user_id: int

    class Config:
        orm_mode = True

class WorkoutPlanCreate(WorkoutPlanBase):
    exercises_workout_plan: List[ExerciseWorkoutPlanCreate]

class WorkoutPlanCreated(WorkoutPlanBase):
    exercises_workout_plan: List[ExerciseWorkoutPlan]
    id: int

class WorkoutPlanUpdate(WorkoutPlanBase):
    id: int

class WorkoutPlan(WorkoutPlanBase):
    id: int

class WorkoutPlanWithUser(WorkoutPlan):
    user: User
