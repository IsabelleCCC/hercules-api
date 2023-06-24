from pydantic import BaseModel

class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(ExerciseBase):
    id: int


class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True
