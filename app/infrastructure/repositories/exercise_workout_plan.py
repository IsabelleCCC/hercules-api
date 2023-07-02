from sqlalchemy.orm import Session, join, aliased
from sqlalchemy import func
from fastapi import Depends
from typing import List, Optional
from core.models.exercise import Exercise as ExerciseModel
from core.models.workout import Workout as WorkoutModel
from core.models.exercise_workout_plan import ExerciseWorkoutPlan as ExerciseWorkoutPlanModel
from core.schemas.exercise_workout_plan import ExerciseWorkoutPlanCreate, ExerciseWorkoutPlanUpdate, ExerciseWorkoutPlan, ExerciseWorkoutPlanWithName
from infrastructure.configs.database import get_db


class ExerciseWorkoutPlanRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, exercise_workout_plan: ExerciseWorkoutPlanCreate) -> ExerciseWorkoutPlan:
        db_exercise_workout_plan = ExerciseWorkoutPlanModel(exercise_id=exercise_workout_plan.exercise_id,
                                                            workout_plan_id=exercise_workout_plan.workout_plan_id,
                                                            sets=exercise_workout_plan.sets,
                                                            reps=exercise_workout_plan.reps,
                                                            combination=exercise_workout_plan.combination)
        self.db.add(db_exercise_workout_plan)
        self.db.commit()
        self.db.refresh(db_exercise_workout_plan)
        return db_exercise_workout_plan

    def get_with_name(self, id: int) -> ExerciseWorkoutPlanWithName:
        response = self.db.query(
            ExerciseWorkoutPlanModel.id,
            ExerciseWorkoutPlanModel.sets,
            ExerciseWorkoutPlanModel.reps,
            ExerciseWorkoutPlanModel.exercise_id,
            ExerciseWorkoutPlanModel.workout_plan_id,
            ExerciseWorkoutPlanModel.combination,
            WorkoutModel.id.label('workout_id'),
            ExerciseModel.name.label('exercise_name'),
            WorkoutModel.reps.label('workout_reps'),
            WorkoutModel.max_weight.label('workout_max_weight'))\
        .join(ExerciseModel, ExerciseModel.id == ExerciseWorkoutPlanModel.exercise_id) \
        .outerjoin(WorkoutModel, (WorkoutModel.workout_exercise_id == ExerciseWorkoutPlanModel.id) & (func.DATE(WorkoutModel.datetime) == func.CURRENT_DATE())) \
        .filter(ExerciseWorkoutPlanModel.id == id) \
        .first()

        return response

    def get(self, id: int) -> ExerciseWorkoutPlan:
        return self.db.query(ExerciseWorkoutPlanModel).filter(ExerciseWorkoutPlanModel.id == id).first()

    def list(self, workout_plan_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[ExerciseWorkoutPlanWithName]:
        response = self.db.query(
            ExerciseWorkoutPlanModel.id,
            ExerciseWorkoutPlanModel.sets,
            ExerciseWorkoutPlanModel.reps,
            ExerciseWorkoutPlanModel.exercise_id,
            ExerciseWorkoutPlanModel.workout_plan_id,
            ExerciseWorkoutPlanModel.combination,
            WorkoutModel.id.label('workout_id'),
            ExerciseModel.name.label('exercise_name'),
            WorkoutModel.reps.label('workout_reps'),
            WorkoutModel.max_weight.label('workout_max_weight'))\
        .join(ExerciseModel, ExerciseModel.id == ExerciseWorkoutPlanModel.exercise_id) \
        .outerjoin(WorkoutModel, (WorkoutModel.workout_exercise_id == ExerciseWorkoutPlanModel.id) & (func.DATE(WorkoutModel.datetime) == func.CURRENT_DATE())) \
        .filter(ExerciseWorkoutPlanModel.workout_plan_id == workout_plan_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

        return response

    def update(self, exercise_workout_plan: ExerciseWorkoutPlanUpdate) -> ExerciseWorkoutPlanUpdate:
        self.db.merge(exercise_workout_plan)
        self.db.commit()
        return exercise_workout_plan

    def delete(self, exercise_workout_plan: ExerciseWorkoutPlan) -> bool:
        self.db.delete(exercise_workout_plan)
        self.db.commit()
        self.db.flush()
