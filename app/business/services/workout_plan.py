from fastapi import Depends
from core.models.workout_plan import WorkoutPlan as WorkoutPlan
from core.schemas.workout_plan import WorkoutPlanCreate, WorkoutPlanUpdate, WorkoutPlanCreated
from infrastructure.repositories.workout_plan import WorkoutPlanRepository
from business.services.exceptions import NotFoundException
from typing import List, Optional


class WorkoutPlanService:
    workoutPlanRepository: WorkoutPlanRepository

    def __init__(self, workoutPlanRepository: WorkoutPlanRepository = Depends()) -> None:
        self.workoutPlanRepository = workoutPlanRepository

    def create(self, workout_plan_body: WorkoutPlanCreate) -> WorkoutPlanCreated:
        return self.workoutPlanRepository.create(workout_plan_body)

    def get(self, workout_plan_id: int) -> WorkoutPlan:
        workout_plan = self.workoutPlanRepository.get(workout_plan_id)
        if not workout_plan:
            raise NotFoundException()
        return workout_plan

    def update(self, workout_plan_body: WorkoutPlanUpdate) -> WorkoutPlan:
        workout_plan = self.workoutPlanRepository.get(workout_plan_body.id)

        if not workout_plan:
            raise NotFoundException()

        return self.workoutPlanRepository.update(WorkoutPlan(id=workout_plan_body.id,
                                                             name=workout_plan_body.name,
                                                             start_date=workout_plan_body.start_date,
                                                             end_date=workout_plan_body.end_date,
                                                             user_id=workout_plan_body.user_id))

    def delete(self, workout_plan_id: int) -> None:
        workout_plan = self.workoutPlanRepository.get(workout_plan_id)

        if not workout_plan:
            raise NotFoundException()

        return self.workoutPlanRepository.delete(workout_plan)

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[WorkoutPlan]:
        workout_plan_list = self.workoutPlanRepository.list(user_id, skip, limit)

        if len(workout_plan_list) == 0:
            raise NotFoundException()

        return workout_plan_list
