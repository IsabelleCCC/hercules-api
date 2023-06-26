from fastapi import Depends
from core.models.workout import Workout
from core.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutWithExercise
from infrastructure.repositories.workout import WorkoutRepository
from business.services.exceptions import NotFoundException
from typing import List, Optional


class WorkoutService:
    workoutRepository: WorkoutRepository

    def __init__(self, workoutRepository: WorkoutRepository = Depends()) -> None:
        self.workoutRepository = workoutRepository

    def create(self, workout_body: WorkoutCreate) -> Workout:
        return self.workoutRepository.create(Workout(workout_exercise_id=workout_body.workout_exercise_id,
                                                     datetime=workout_body.datetime,
                                                     reps=workout_body.reps,
                                                     max_weight=workout_body.max_weight))

    def get(self, workout_id: int) -> WorkoutWithExercise:
        workout = self.workoutRepository.get_with_exercise(workout_id)
        if not workout:
            raise NotFoundException()
        return workout

    def update(self, workout_body: WorkoutUpdate) -> WorkoutWithExercise:
        workout = self.workoutRepository.get(workout_body.id)

        if not workout:
            raise NotFoundException()

        updated = self.workoutRepository.update(Workout(id=workout_body.id,
                                                        workout_exercise_id=workout_body.workout_exercise_id,
                                                        datetime=workout_body.datetime,
                                                        reps=workout_body.reps,
                                                        max_weight=workout_body.max_weight))

        return self.workoutRepository.get_with_exercise(updated.id)

    def delete(self, workout_id: int) -> None:
        workout = self.workoutRepository.get(workout_id)

        if not workout:
            raise NotFoundException()

        return self.workoutRepository.delete(workout)

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[WorkoutWithExercise]:
        workout_list = self.workoutRepository.list(user_id, skip, limit)

        if len(workout_list) == 0:
            raise NotFoundException()

        return workout_list
