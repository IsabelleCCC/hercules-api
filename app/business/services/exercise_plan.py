from fastapi import Depends
from core.models.exercise_plan import ExercisePlan
from core.schemas.exercise_plan import ExercisePlanCreate, ExercisePlanUpdate, ExercisePlanWithName
from infrastructure.repositories.exercise_plan import ExercisePlanRepository
from business.services.exceptions import NotFoundException
from typing import List, Optional


class ExercisePlanService:
    exercisePlanRepository: ExercisePlanRepository

    def __init__(self, exercisePlanRepository: ExercisePlanRepository = Depends()) -> None:
        self.exercisePlanRepository = ExercisePlanRepository

    def create(self, exercise_plan_body: ExercisePlanCreate) -> ExercisePlan:
        return self.exercisePlanRepository.create(ExercisePlan(exercise_id = exercise_plan_body.exercise_id,
                                                                             workout_plan_id = exercise_plan_body.workout_plan_id,
                                                                             sets = exercise_plan_body.sets,
                                                                             reps = exercise_plan_body.reps,
                                                                             combination = exercise_plan_body.combination))

    def get(self, workout_plan_id: int) -> ExercisePlanWithName:
        exercise_plan = self.exercisePlanRepository.list_with_name_by_workout_plan(workout_plan_id)
        if not exercise_plan:
            raise NotFoundException()
        return exercise_plan

    def update(self, exercise_plan_body: ExercisePlanUpdate) -> ExercisePlanWithName:
        exercise_plan = self.exercisePlanRepository.get(exercise_plan_body.id)

        if not exercise_plan:
            raise NotFoundException()

        updated = self.exercisePlanRepository.update(ExercisePlan(id = exercise_plan_body.id,
                                                                             exercise_id = exercise_plan_body.exercise_id,
                                                                             workout_plan_id = exercise_plan_body.workout_plan_id,
                                                                             sets = exercise_plan_body.sets,
                                                                             reps = exercise_plan_body.reps,
                                                                             combination = exercise_plan_body.combination))

        return self.exercisePlanRepository.list_with_name_by_workout_plan(updated.id)

    def delete(self, exercise_plan_id: int) -> None:
        exercise_plan = self.exercisePlanRepository.get(exercise_plan_id)

        if not exercise_plan:
            raise NotFoundException()

        return self.exercisePlanRepository.delete(exercise_plan)

    # def list(self, workout_plan_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[ExercisePlanWithName]:
    #     exercise_plan_list = self.exercisePlanRepository.list(workout_plan_id, skip, limit)

    #     if len(exercise_plan_list) == 0:
    #         raise NotFoundException()

    #     return exercise_plan_list
