from sqlalchemy.orm import Session, join, aliased
from sqlalchemy import func
from fastapi import Depends
from typing import List, Optional
from core.models.exercise import Exercise as ExerciseModel
from core.models.workout_plan import WorkoutPlan as WorkoutPlanModel
from core.models.exercise_plan import ExercisePlan as ExercisePlanModel
from core.schemas.exercise_plan import ExercisePlanCreate, ExercisePlanUpdate, ExercisePlan, ExercisePlanWithName
from infrastructure.configs.database import get_db


class ExercisePlanRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, exercise_plan: ExercisePlanCreate) -> ExercisePlan:
        db_exercise_plan = ExercisePlanModel(exercise_id=exercise_plan.exercise_id,
                                                            workout_plan_id=exercise_plan.workout_plan_id,
                                                            sets=exercise_plan.sets,
                                                            reps=exercise_plan.reps,
                                                            combination=exercise_plan.combination)
        self.db.add(db_exercise_plan)
        self.db.commit()
        self.db.refresh(db_exercise_plan)
        return db_exercise_plan

    def list_with_name_by_workout_plan(self, workout_plan_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> list[ExercisePlanWithName]:
        response = self.db.query(
            ExercisePlanModel.id,
            ExercisePlanModel.sets,
            ExercisePlanModel.reps,
            ExercisePlanModel.exercise_id,
            ExercisePlanModel.workout_plan_id,
            ExercisePlanModel.combination,
                ExerciseModel.name.label('exercise_name'),
            WorkoutPlanModel.reps.label('workout_plan_id'))\
        .join(ExerciseModel, ExerciseModel.id == ExercisePlanModel.exercise_id) \
        .outerjoin(WorkoutPlanModel,(WorkoutPlanModel.id == ExercisePlanModel.workout_plan_id)) \
        .filter(WorkoutPlanModel.id == workout_plan_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

        return response

    def get(self, id: int) -> ExercisePlan:
        return self.db.query(ExercisePlanModel).filter(ExercisePlanModel.id == id).first()

    def update(self, exercise_plan: ExercisePlanUpdate) -> ExercisePlanUpdate:
        self.db.merge(exercise_plan)
        self.db.commit()
        return exercise_plan

    def delete(self, exercise_plan: ExercisePlan) -> bool:
        self.db.delete(exercise_plan)
        self.db.commit()
        self.db.flush()
