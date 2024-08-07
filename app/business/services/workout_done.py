from fastapi import Depends
from core.models.workout_done import WorkoutDone
from core.schemas.workout_done import WorkoutDoneCreate, WorkoutDoneUpdate, WorkoutDoneWithPagination
from infrastructure.repositories.workout_done import WorkoutDoneRepository
from business.services.exceptions import NotFoundException, BadRequestException
from typing import List, Optional


class WorkoutDoneService:
    workoutDoneRepository: WorkoutDoneRepository

    def __init__(self, workoutDoneRepository: WorkoutDoneRepository = Depends()) -> None:
        self.workoutDoneRepository = workoutDoneRepository

    def create(self, workout_done_body: WorkoutDoneCreate) -> WorkoutDone:
        return self.workoutDoneRepository.create(workout_done_body)

    def get(self, workout_id: int) -> WorkoutDone:
        workout_done = self.workoutDoneRepository.get_with_exercise(workout_id)
        if not workout_done:
            raise NotFoundException()
        return workout_done

    def update(self, workout_body: WorkoutDoneUpdate) -> WorkoutDone:
        workout_done = self.workoutDoneRepository.get(workout_body.id)

        if not workout_done:
            raise NotFoundException()

        updated = self.workoutDoneRepository.update(WorkoutDone(id=workout_body.id,
                                                        workout_exercise_id=workout_body.workout_exercise_id,
                                                        datetime=workout_body.datetime,
                                                        reps=workout_body.reps,
                                                        max_weight=workout_body.max_weight))

        return self.workoutDoneRepository.get_with_exercise(updated.id)

    def delete(self, workout_id: int) -> None:
        workout_done = self.workoutDoneRepository.get(workout_id)

        if not workout_done:
            raise NotFoundException()

        return self.workoutDoneRepository.delete(workout_done)

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> WorkoutDoneWithPagination:
        response = self.workoutDoneRepository.list(user_id, skip, limit)

        if len(response.workouts_done) == 0:
            raise NotFoundException()

        return response
