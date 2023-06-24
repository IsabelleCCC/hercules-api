from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Optional
from core.models.fitness_test import FitnessTest as FitnessTestModel
from core.schemas.fitness_test import FitnessTestCreate, FitnessTestUpdate, FitnessTest
from ..configs.database import get_db

class FitnessTestRepository:
    db: Session

    def __init__(self, db: Session=Depends(get_db)) -> None:
        self.db = db

    def create(self, fitness_test: FitnessTestCreate) -> FitnessTest:
        db_fitness_test = FitnessTestModel(
            user_id=fitness_test.user_id,
            date=fitness_test.date,
            weight=fitness_test.weight,
            body_fat=fitness_test.body_fat,
            chest=fitness_test.chest,
            right_arm_contr=fitness_test.right_arm_contr,
            left_arm_contr=fitness_test.left_arm_contr,
            hip=fitness_test.hip,
            right_arm_relax=fitness_test.right_arm_relax,
            left_arm_relax=fitness_test.left_arm_relax,
            abdomen=fitness_test.abdomen,
            waist=fitness_test.waist,
            right_forearm=fitness_test.right_forearm,
            left_forearm=fitness_test.left_forearm,
            right_thigh=fitness_test.right_thigh,
            left_thigh=fitness_test.left_thigh,
            scapular=fitness_test.scapular,
            right_calf=fitness_test.right_calf,
            left_calf=fitness_test.left_calf,
            observations=fitness_test.observations
        )

        self.db.add(db_fitness_test)
        self.db.commit()
        self.db.refresh(db_fitness_test)
        return db_fitness_test

    def get(self, fitness_test_id: int) -> FitnessTest:
        return self.db.query(FitnessTestModel).filter(FitnessTestModel.id == fitness_test_id).first()

    def list(self, user_id: int, skip: int = 0, limit: int = 100) -> List[FitnessTest]:
        return self.db.query(FitnessTestModel).filter(FitnessTestModel.user_id == user_id).offset(skip).limit(limit).all()

    def update(self, fitness_test: FitnessTestUpdate) -> FitnessTest:
        self.db.merge(fitness_test)
        self.db.commit()
        return fitness_test

    def delete(self, fitness_test: FitnessTest) -> None:
        self.db.delete(fitness_test)
        self.db.commit()
        self.db.flush()
