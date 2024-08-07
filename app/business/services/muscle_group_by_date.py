from fastapi import Depends
from core.schemas.muscle_group_by_date import MuscleGroupByDate
from infrastructure.repositories.muscle_group_by_date import MuscleGroupByDateRepository
from business.services.exceptions import NotFoundException
from typing import List, Optional


class MuscleGroupByDateService:
    muscleGroupRepository: MuscleGroupByDateRepository

    def __init__(self, muscleGroupRepository: MuscleGroupByDateRepository = Depends()) -> None:
        self.muscleGroupRepository = muscleGroupRepository

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[MuscleGroupByDate]:
        muscle_group_list = self.muscleGroupRepository.list(user_id, skip, limit)

        if len(muscle_group_list) == 0:
            raise NotFoundException()

        return muscle_group_list
