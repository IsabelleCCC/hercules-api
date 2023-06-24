from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.services.auth import AuthService
from app.services.exercise_workout_plan import ExerciseWorkoutPlanService
from app.services.exceptions import NotFoundException
from core.schemas.exercise_workout_plan import ExerciseWorkoutPlanCreate, ExerciseWorkoutPlanUpdate, ExerciseWorkoutPlan, ExerciseWorkoutPlanWithName

ExerciseWorkoutPlanRouter = APIRouter(
    prefix='/exercise-workout-plan', tags=['exercise-workout-plan']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@ExerciseWorkoutPlanRouter.get("/{exercise_workout_plan_id}", response_model=ExerciseWorkoutPlanWithName)
def get(exercise_workout_plan_id: int, exercise_workout_plan_service: ExerciseWorkoutPlanService = Depends()):
    try:
        exercise_workout_plan = exercise_workout_plan_service.get(exercise_workout_plan_id)
        return exercise_workout_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@ExerciseWorkoutPlanRouter.get("", response_model=List[ExerciseWorkoutPlanWithName])
def list(workout_plan_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, exercise_workout_plan_service: ExerciseWorkoutPlanService = Depends()):
    try:
        workout_plan = exercise_workout_plan_service.list(workout_plan_id, skip, limit)
        return workout_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro associado a esse plano de treino.")


@ExerciseWorkoutPlanRouter.post("", response_model=ExerciseWorkoutPlan)
def create(exercise_workout_plan_body: ExerciseWorkoutPlanCreate, exercise_workout_plan_service: ExerciseWorkoutPlanService = Depends()):
    exercise_workout_plan = exercise_workout_plan_service.create(exercise_workout_plan_body)
    return exercise_workout_plan


@ExerciseWorkoutPlanRouter.put("", response_model=ExerciseWorkoutPlanWithName)
def update(exercise_workout_plan_body: ExerciseWorkoutPlanUpdate, exercise_workout_plan_service: ExerciseWorkoutPlanService = Depends()):
    try:
        exercise_workout_plan = exercise_workout_plan_service.update(exercise_workout_plan_body)
        return exercise_workout_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@ExerciseWorkoutPlanRouter.delete("/{exercise_workout_plan_id}")
def delete(exercise_workout_plan_id: int, exercise_workout_plan_service: ExerciseWorkoutPlanService = Depends()):
    try:
        exercise_workout_plan_service.delete(exercise_workout_plan_id)
        return {"message": "Registro deletado."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
