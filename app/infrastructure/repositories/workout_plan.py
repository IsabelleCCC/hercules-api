from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import Depends
from core.models.workout_plan import WorkoutPlan as WorkoutPlanModel
from core.schemas.workout_plan import WorkoutPlanCreate, WorkoutPlanUpdate, WorkoutPlanCreated, WorkoutPlanWithExercisePlan
from core.models.exercise_plan import ExercisePlan as ExercisePlanModel
from infrastructure.configs.database import get_db
from typing import List
from sqlalchemy.orm import lazyload

class WorkoutPlanRepository:
    db: Session

    def __init__(self, db: Session=Depends(get_db)) -> None:
        self.db = db

    def create(self, workout_plan: WorkoutPlanCreate) -> WorkoutPlanWithExercisePlan:
        db_workout_plan = WorkoutPlanModel(
            name=workout_plan.name,
            start_date=workout_plan.start_date,
            end_date=workout_plan.end_date,
            user_id=workout_plan.user_id)

        self.db.add(db_workout_plan)
        self.db.flush()

        exercise_plan_list = [
            ExercisePlanModel(
                exercise_id=obj.exercise_id,
                workout_plan_id=db_workout_plan.id,
                sets=obj.sets,
                reps=obj.reps,
                combination=obj.combination,
            )
            for obj in workout_plan.exercise_plans
        ]

        self.db.add_all(exercise_plan_list)
        self.db.commit()
        self.db.refresh(db_workout_plan)

        return db_workout_plan

    def get(self, workout_plan_id: int) -> WorkoutPlanWithExercisePlan:
        return self.db.query(
            WorkoutPlanModel).options(lazyload(WorkoutPlanModel.exercise_plans)) \
        .outerjoin(ExercisePlanModel, ExercisePlanModel.workout_plan_id == WorkoutPlanModel.id) \
        .filter(WorkoutPlanModel.id == workout_plan_id).order_by(desc(WorkoutPlanModel.start_date)).first()

    def update(self, workout_plan: WorkoutPlanUpdate) -> WorkoutPlanModel:
        self.db.merge(workout_plan)
        self.db.commit()
        self.db.flush()
        return workout_plan

    def list(self, user_id: int, skip: int = 0, limit: int = 100) -> List[WorkoutPlanWithExercisePlan]:
        return self.db.query(
            WorkoutPlanModel).options(lazyload(WorkoutPlanModel.exercise_plans)) \
        .outerjoin(ExercisePlanModel, ExercisePlanModel.workout_plan_id == WorkoutPlanModel.id) \
        .filter(WorkoutPlanModel.user_id == user_id).order_by(desc(WorkoutPlanModel.start_date)).offset(skip).limit(limit).all()

    def delete(self, workout_plan: WorkoutPlanModel) -> None:
        self.db.delete(workout_plan)
        self.db.commit()
        self.db.flush()
