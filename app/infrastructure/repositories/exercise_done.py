from sqlalchemy.orm import Session, join, aliased
from sqlalchemy import func
from fastapi import Depends
from typing import List, Optional
from core.models.workout_plan import WorkoutPlan as WorkoutPlanModel
from core.models.exercise import Exercise as ExerciseModel
from core.models.workout_done import WorkoutDone as WorkoutDoneModel
from core.models.exercise_plan import ExercisePlan as ExercisePlanModel
from core.models.exercise_done import ExerciseDone as ExerciseDoneModel
from core.schemas.exercise_done import ExerciseDone as ExerciseDone, ExerciseDoneByUser, ExerciseDoneCreate, ExerciseDoneWithName, ExerciseDoneWithPagination
from infrastructure.configs.database import get_db


class ExerciseDoneRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, exerciseDoneList: List[ExerciseDoneCreate]) -> List[ExerciseDone]:
        db_exercise_done = [
            ExerciseDoneModel(reps=exercise_done.reps,
                            max_weight=exercise_done.max_weight,
                            workout_done_id=exercise_done.workout_done_id,
                            exercise_plan_id=exercise_done.exercise_plan_id)
            for exercise_done in exerciseDoneList
        ]

        self.db.add_all(db_exercise_done)
        self.db.commit()
        return db_exercise_done


    def list_by_workout_done(self, workout_done_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> list[ExerciseDoneWithName]:
        response = self.db.query(
            ExerciseDoneModel.id,
            ExerciseDoneModel.reps,
            ExerciseDoneModel.max_weight,
            ExerciseDoneModel.workout_done_id,
            ExerciseDoneModel.exercise_plan_id,
            ExerciseModel.name.label('exercise_name'),
            ExerciseModel.muscle_group)\
        .join(ExercisePlanModel, ExercisePlanModel.id == ExerciseDoneModel.exercise_plan_id) \
        .join(ExerciseModel, ExerciseModel.id == ExercisePlanModel.exercise_id) \
        .filter(WorkoutDoneModel.id == workout_done_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

        return response

    def list_by_user_id(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> list[ExerciseDoneWithPagination]:
        exercises = self.db.query(
            ExerciseDoneModel.id,
            ExerciseDoneModel.reps,
            ExerciseDoneModel.max_weight,
            ExerciseDoneModel.workout_done_id,
            ExerciseDoneModel.exercise_plan_id,
            ExerciseModel.name.label('exercise_name'),
            ExerciseModel.muscle_group,
            WorkoutDoneModel.datetime)\
        .join(ExercisePlanModel, ExercisePlanModel.id == ExerciseDoneModel.exercise_plan_id) \
        .join(ExerciseModel, ExerciseModel.id == ExercisePlanModel.exercise_id) \
        .join(WorkoutPlanModel, ExercisePlanModel.workout_plan_id == WorkoutPlanModel.id) \
        .join(WorkoutDoneModel, WorkoutPlanModel.id == WorkoutDoneModel.workout_plan_id) \
        .filter(WorkoutPlanModel.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

        count_exercises = self.db.query(func.count(ExerciseDoneModel.id))\
        .join(ExercisePlanModel, ExercisePlanModel.id == ExerciseDoneModel.exercise_plan_id) \
        .join(ExerciseModel, ExerciseModel.id == ExercisePlanModel.exercise_id) \
        .join(WorkoutPlanModel, ExercisePlanModel.workout_plan_id == WorkoutPlanModel.id) \
        .join(WorkoutDoneModel, WorkoutPlanModel.id == WorkoutDoneModel.workout_plan_id) \
        .filter(WorkoutPlanModel.user_id == user_id) \
        .scalar()

        return ExerciseDoneWithPagination(
            count=count_exercises,
            response=exercises
        )

    def delete(self, exercise_done: ExerciseDone) -> bool:
        self.db.delete(exercise_done)
        self.db.commit()
        self.db.flush()

    def get(self, id: int) -> ExerciseDone:
        return self.db.query(ExerciseDoneModel).filter(ExerciseDoneModel.id == id).first()
