from pydantic import BaseModel

class MuscleGroupByDateBase(BaseModel):
    user_id: int
    muscle_group: str
    count: int
    week_of_month: str
    orderby: str


class MuscleGroupByDate(MuscleGroupByDateBase):
    class Config:
        orm_mode = True
