from fastapi import Depends
from typing import Optional, List
from infrastructure.repositories.exercise import ExerciseRepository
from core.models.exercise import Exercise
from core.schemas.exercise import ExerciseCreate, ExerciseUpdate
from app.services.exceptions import NotFoundException


class ExerciseService:
    exerciseRepository: ExerciseRepository

    def __init__(self, exerciseRepository: ExerciseRepository = Depends()) -> None:
        self.exerciseRepository = exerciseRepository

    def create(self, exercise_body: ExerciseCreate) -> Exercise:
        return self.exerciseRepository.create(Exercise(name=exercise_body.name))

    def get(self, exercise_id: int) -> Exercise:
        exercise = self.exerciseRepository.get(exercise_id)
        if not exercise:
            raise NotFoundException()

        return exercise

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[Exercise]:
        exercise_list = self.exerciseRepository.list(skip, limit)

        if len(exercise_list) == 0:
            raise NotFoundException()

        return exercise_list

    def update(self, exercise_body: ExerciseUpdate) -> Exercise:
        exercise = self.exerciseRepository.get(exercise_body.id)
        if not exercise:
            raise NotFoundException()

        return self.exerciseRepository.update(Exercise(name=exercise_body.name, id=exercise.id))

    def delete(self, exercise_id: int):
        exercise = self.exerciseRepository.get(exercise_id)
        if not exercise:
            raise NotFoundException()
        return self.exerciseRepository.delete(exercise)
