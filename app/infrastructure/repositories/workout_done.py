from sqlalchemy import func
from sqlalchemy.orm import Session, join, aliased
from fastapi import Depends
from typing import List, Optional
from core.models.exercise_done import ExerciseDone as ExerciseDoneModel
from core.models.exercise import Exercise
from core.models.exercise_plan import ExercisePlan
from core.models.workout_done import WorkoutDone as WorkoutDoneModel
from core.models.workout_plan import WorkoutPlan
from core.models.user import User
from core.schemas.workout_done import WorkoutDoneCreate, WorkoutDoneUpdate, WorkoutDone, WorkoutDoneWithName, WorkoutDoneWithPagination
from infrastructure.configs.database import get_db


class WorkoutDoneRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, workout_done: WorkoutDoneCreate) -> WorkoutDone:
        db_workout_done = WorkoutDoneModel(
            datetime=workout_done.datetime,
            duration=workout_done.duration,
            workout_plan_id=workout_done.workout_plan_id
        )

        self.db.add(db_workout_done)
        self.db.flush()

        exercises_done = [
            ExerciseDoneModel(
                reps=obj.reps,
                max_weight=obj.max_weight,
                workout_done_id=db_workout_done.id,
                exercise_plan_id=obj.exercise_plan_id
            )
            for obj in workout_done.exercises_done
        ]

        self.db.add_all(exercises_done)
        self.db.commit()
        self.db.refresh(db_workout_done)

        return db_workout_done

    def get_with_name(self, id: int) -> WorkoutDoneWithName:
        response = self.db.query(
            WorkoutDoneModel.id,
            WorkoutDoneModel.datetime,
            WorkoutDoneModel.duration,
            WorkoutDoneModel.user_id,
            WorkoutDoneModel.workout_plan_id,
            WorkoutPlan.name.label('workout_name')) \
            .join(WorkoutPlan, WorkoutPlan.id == WorkoutDoneModel.workout_plan_id) \
            .filter(WorkoutDoneModel.id == id).first()

        return response

    def get(self, id: int) -> WorkoutDone:
        return self.db.query(WorkoutDoneModel).filter(WorkoutDoneModel.id == id).first()

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> WorkoutDoneWithPagination:
        workouts = self.db.query(
            WorkoutDoneModel.id,
            WorkoutDoneModel.datetime,
            WorkoutDoneModel.duration,
            WorkoutDoneModel.workout_plan_id,
            WorkoutPlan.name.label('workout_name')) \
            .join(WorkoutPlan, WorkoutPlan.id == WorkoutDoneModel.workout_plan_id) \
            .join(User, WorkoutPlan.user_id == User.id) \
            .filter(User.id == user_id) \
            .order_by(WorkoutDoneModel.datetime.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

        count_workouts = self.db.query(func.count(WorkoutDoneModel.id))\
        .join(WorkoutPlan, WorkoutPlan.id == WorkoutDoneModel.workout_plan_id) \
            .join(User, WorkoutPlan.user_id == User.id) \
            .filter(User.id == user_id) \
            .order_by(WorkoutDoneModel.datetime.desc()) \
            .scalar()

        response = WorkoutDoneWithPagination(
            count=count_workouts,
            workouts_done=workouts
        )

        return response


    def update(self, workout: WorkoutDoneUpdate) -> WorkoutDoneUpdate:
        self.db.merge(workout)
        self.db.commit()
        return workout

    def delete(self, workout: WorkoutDone) -> bool:
        self.db.delete(workout)
        self.db.commit()
        self.db.flush()
