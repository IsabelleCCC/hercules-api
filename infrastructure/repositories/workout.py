from sqlalchemy.orm import Session, join, aliased
from fastapi import Depends
from typing import List, Optional
from core.models.exercise import Exercise
from core.models.exercise_workout_plan import ExerciseWorkoutPlan
from core.models.workout import Workout as WorkoutModel
from core.models.workout_plan import WorkoutPlan
from core.schemas.workout import WorkoutCreate, WorkoutUpdate, Workout, WorkoutWithExercise
from infrastructure.configs.database import get_db


class WorkoutRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, workout: WorkoutCreate) -> Workout:
        db_workout = WorkoutModel(workout_exercise_id=workout.workout_exercise_id,
                                  datetime=workout.datetime,
                                  reps=workout.reps,
                                  max_weight=workout.max_weight)
        self.db.add(db_workout)
        self.db.commit()
        self.db.refresh(db_workout)
        return db_workout

    def get_with_exercise(self, id: int) -> WorkoutWithExercise:
        response = self.db.query(
            WorkoutModel.id,
            WorkoutModel.datetime,
            WorkoutModel.workout_exercise_id,
            WorkoutModel.reps,
            WorkoutModel.max_weight,
            Exercise.name.label('exercise_name')) \
            .join(ExerciseWorkoutPlan, ExerciseWorkoutPlan.id == WorkoutModel.workout_exercise_id) \
            .join(Exercise, Exercise.id == ExerciseWorkoutPlan.exercise_id) \
            .join(WorkoutPlan, WorkoutPlan.id == ExerciseWorkoutPlan.workout_plan_id) \
            .filter(WorkoutModel.id == id).first()

        return response

    def get(self, id: int) -> Workout:
        return self.db.query(WorkoutModel).filter(WorkoutModel.id == id).first()

    def list(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[WorkoutWithExercise]:
        response = self.db.query(
            WorkoutModel.id,
            WorkoutModel.datetime,
            WorkoutModel.workout_exercise_id,
            WorkoutModel.reps,
            WorkoutModel.max_weight,
            Exercise.name.label('exercise_name')) \
            .join(ExerciseWorkoutPlan, ExerciseWorkoutPlan.id == WorkoutModel.workout_exercise_id) \
            .join(Exercise, Exercise.id == ExerciseWorkoutPlan.exercise_id) \
            .join(WorkoutPlan, WorkoutPlan.id == ExerciseWorkoutPlan.workout_plan_id) \
            .filter(WorkoutPlan.user_id == user_id) \
            .offset(skip) \
            .limit(limit) \
            .all()

        return response

    def update(self, workout: WorkoutUpdate) -> WorkoutUpdate:
        self.db.merge(workout)
        self.db.commit()
        return workout

    def delete(self, workout: Workout) -> bool:
        self.db.delete(workout)
        self.db.commit()
        self.db.flush()
