from pydantic import BaseModel
from typing import List
from datetime import date
from core.schemas.user import User

class WorkoutPlanBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    user_id: int

class WorkoutPlanCreate(WorkoutPlanBase):
    pass

class WorkoutPlanUpdate(WorkoutPlanBase):
    id: int

class WorkoutPlan(WorkoutPlanBase):
    id: int

    class Config:
        orm_mode = True

class WorkoutPlanWithUser(WorkoutPlan):
    user: User
