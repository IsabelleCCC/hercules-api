from pydantic import BaseModel
from typing import Optional
from datetime import date


class FitnessTestBase(BaseModel):
    user_id: int
    date: date
    weight: float
    body_fat: Optional[float]
    chest: Optional[float]
    right_arm_contr: Optional[float]
    left_arm_contr: Optional[float]
    hip: Optional[float]
    right_arm_relax: Optional[float]
    left_arm_relax: Optional[float]
    abdomen: Optional[float]
    waist: Optional[float]
    right_forearm: Optional[float]
    left_forearm: Optional[float]
    right_thigh: Optional[float]
    left_thigh: Optional[float]
    scapular: Optional[float]
    right_calf: Optional[float]
    left_calf: Optional[float]
    observations: Optional[str]


class FitnessTestCreate(FitnessTestBase):
    pass


class FitnessTestUpdate(FitnessTestBase):
    id: int


class FitnessTest(FitnessTestBase):
    id: int

    class Config:
        orm_mode = True
