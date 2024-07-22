from fastapi import Depends
from core.schemas.exercise_done import ExerciseDoneCreate, ExerciseDone, ExerciseDoneWithName
from infrastructure.repositories.exercise_done import ExerciseDoneRepository
from business.services.exceptions import NotFoundException
from typing import List, Optional


class ExerciseDoneService:
    exerciseDoneRepository: ExerciseDoneRepository

    def __init__(self, exerciseDoneRepository: ExerciseDoneRepository = Depends()) -> None:
        self.exerciseDoneRepository = exerciseDoneRepository

    def create(self, exercise_done_body: ExerciseDoneCreate) -> ExerciseDone:
        return self.exerciseDoneRepository.create(ExerciseDone(reps=exercise_done_body.reps,
                                                            max_weight=exercise_done_body.max_weight,
                                                            datetime=exercise_done_body.datetime,
                                                            workout_done_id=exercise_done_body.workout_done_id,
                                                            exercise_plan_id=exercise_done_body.exercise_plan_id))

    def delete(self, exercise_done_id: int) -> None:
        exercise_plan = self.exerciseDoneRepository.get(exercise_done_id)

        if not exercise_plan:
            raise NotFoundException()

        return self.exerciseDoneRepository.delete(exercise_plan)

    def list(self, workout_done_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[ExerciseDoneWithName]:
        exercise_done_list = self.exerciseDoneRepository.list(workout_done_id, skip, limit)

        if len(exercise_done_list) == 0:
            raise NotFoundException()

        return exercise_done_list
