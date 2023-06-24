from fastapi import Depends
from typing import Optional, List
from infrastructure.repositories.fitness_test import FitnessTestRepository
from core.models.fitness_test import FitnessTest
from core.schemas.fitness_test import FitnessTestCreate, FitnessTestUpdate
from app.services.exceptions import NotFoundException


class FitnessTestService:
    fitnessTestRepository: FitnessTestRepository

    def __init__(self, fitnessTestRepository: FitnessTestRepository = Depends()) -> None:
        self.fitnessTestRepository = fitnessTestRepository

    def create(self, fitness_test_body: FitnessTestCreate) -> FitnessTest:
        return self.fitnessTestRepository.create(FitnessTest(
            user_id=fitness_test_body.user_id,
            date=fitness_test_body.date,
            weight=fitness_test_body.weight,
            body_fat=fitness_test_body.body_fat,
            chest=fitness_test_body.chest,
            right_arm_contr=fitness_test_body.right_arm_contr,
            left_arm_contr=fitness_test_body.left_arm_contr,
            hip=fitness_test_body.hip,
            right_arm_relax=fitness_test_body.right_arm_relax,
            left_arm_relax=fitness_test_body.left_arm_relax,
            abdomen=fitness_test_body.abdomen,
            waist=fitness_test_body.waist,
            right_forearm=fitness_test_body.right_forearm,
            left_forearm=fitness_test_body.left_forearm,
            right_thigh=fitness_test_body.right_thigh,
            left_thigh=fitness_test_body.left_thigh,
            scapular=fitness_test_body.scapular,
            right_calf=fitness_test_body.right_calf,
            left_calf=fitness_test_body.left_calf,
            observations=fitness_test_body.observations
        ))

    def get(self, fitness_test_id: int) -> FitnessTest:
        fitness_test = self.fitnessTestRepository.get(fitness_test_id)
        if not fitness_test:
            raise NotFoundException()

        return fitness_test

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10) -> List[FitnessTest]:
        fitness_test_list = self.fitnessTestRepository.list(user_id, skip, limit)

        if len(fitness_test_list) == 0:
            raise NotFoundException()

        return fitness_test_list

    def update(self, fitness_test_body: FitnessTestUpdate) -> FitnessTest:
        fitness_test = self.fitnessTestRepository.get(fitness_test_body.id)
        if not fitness_test:
            raise NotFoundException()

        return self.fitnessTestRepository.update(FitnessTest(
            id=fitness_test_body.id,
            user_id=fitness_test_body.user_id,
            date=fitness_test_body.date,
            weight=fitness_test_body.weight,
            body_fat=fitness_test_body.body_fat,
            chest=fitness_test_body.chest,
            right_arm_contr=fitness_test_body.right_arm_contr,
            left_arm_contr=fitness_test_body.left_arm_contr,
            hip=fitness_test_body.hip,
            right_arm_relax=fitness_test_body.right_arm_relax,
            left_arm_relax=fitness_test_body.left_arm_relax,
            abdomen=fitness_test_body.abdomen,
            waist=fitness_test_body.waist,
            right_forearm=fitness_test_body.right_forearm,
            left_forearm=fitness_test_body.left_forearm,
            right_thigh=fitness_test_body.right_thigh,
            left_thigh=fitness_test_body.left_thigh,
            scapular=fitness_test_body.scapular,
            right_calf=fitness_test_body.right_calf,
            left_calf=fitness_test_body.left_calf,
            observations=fitness_test_body.observations
        ))

    def delete(self, fitness_test_id: int):
        fitness_test = self.fitnessTestRepository.get(fitness_test_id)
        if not fitness_test:
            raise NotFoundException()
        return self.fitnessTestRepository.delete(fitness_test)
