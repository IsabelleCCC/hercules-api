from fastapi import Depends
from core.models.exercise_workout_plan import ExerciseWorkoutPlan
from core.schemas.exercise_workout_plan import ExerciseWorkoutPlanCreate, ExerciseWorkoutPlanUpdate, ExerciseWorkoutPlanWithName
from infrastructure.repositories.exercise_workout_plan import ExerciseWorkoutPlanRepository
from app.services.exceptions import NotFoundException
from typing import List, Optional


class ExerciseWorkoutPlanService:
    exerciseWorkoutPlanRepository: ExerciseWorkoutPlanRepository

    def __init__(self, exerciseWorkoutPlanRepository: ExerciseWorkoutPlanRepository = Depends()) -> None:
        self.exerciseWorkoutPlanRepository = exerciseWorkoutPlanRepository

    def create(self, exercise_workout_plan_body: ExerciseWorkoutPlanCreate) -> ExerciseWorkoutPlan:
        return self.exerciseWorkoutPlanRepository.create(ExerciseWorkoutPlan(exercise_id = exercise_workout_plan_body.exercise_id,
                                                                             workout_plan_id = exercise_workout_plan_body.workout_plan_id,
                                                                             sets = exercise_workout_plan_body.sets,
                                                                             reps = exercise_workout_plan_body.reps,
                                                                             combination = exercise_workout_plan_body.combination))

    def get(self, workout_plan_id: int) -> ExerciseWorkoutPlanWithName:
        exercise_workout_plan = self.exerciseWorkoutPlanRepository.get_with_name(workout_plan_id)
        if not exercise_workout_plan:
            raise NotFoundException()
        return exercise_workout_plan

    def update(self, exercise_workout_plan_body: ExerciseWorkoutPlanUpdate) -> ExerciseWorkoutPlanWithName:
        exercise_workout_plan = self.exerciseWorkoutPlanRepository.get(exercise_workout_plan_body.id)

        if not exercise_workout_plan:
            raise NotFoundException()

        updated = self.exerciseWorkoutPlanRepository.update(ExerciseWorkoutPlan(id = exercise_workout_plan_body.id,
                                                                             exercise_id = exercise_workout_plan_body.exercise_id,
                                                                             workout_plan_id = exercise_workout_plan_body.workout_plan_id,
                                                                             sets = exercise_workout_plan_body.sets,
                                                                             reps = exercise_workout_plan_body.reps,
                                                                             combination = exercise_workout_plan_body.combination))

        return self.exerciseWorkoutPlanRepository.get_with_name(updated.id)

    def delete(self, exercise_workout_plan_id: int) -> None:
        exercise_workout_plan = self.exerciseWorkoutPlanRepository.get(exercise_workout_plan_id)

        if not exercise_workout_plan:
            raise NotFoundException()

        return self.exerciseWorkoutPlanRepository.delete(exercise_workout_plan)

    def list(self, workout_plan_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[ExerciseWorkoutPlanWithName]:
        exercise_workout_plan_list = self.exerciseWorkoutPlanRepository.list(workout_plan_id, skip, limit)

        if len(exercise_workout_plan_list) == 0:
            raise NotFoundException()

        return exercise_workout_plan_list
