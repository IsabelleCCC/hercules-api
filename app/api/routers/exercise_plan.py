from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from business.services.auth import AuthService
from business.services.exercise_plan import ExercisePlanService
from business.services.exceptions import NotFoundException
from core.schemas.exercise_plan import ExercisePlanCreate, ExercisePlanUpdate, ExercisePlan, ExercisePlanWithName

ExercisePlanRouter = APIRouter(
    prefix='/exercise-plan', tags=['exercise-plan']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@ExercisePlanRouter.get("/{exercise_plan_id}", response_model=ExercisePlanWithName)
def get(exercise_plan_id: int, exercise_plan_service: ExercisePlanService = Depends()):
    try:
        exercise_plan = exercise_plan_service.get(exercise_plan_id)
        return exercise_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


# @ExercisePlanRouter.get("", response_model=List[ExercisePlanWithName])
# def list(workout_plan_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, exercise_plan_service: ExercisePlanService = Depends()):
#     try:
#         exercise_plan = exercise_plan_service.list(workout_plan_id, skip, limit)
#         return exercise_plan
#     except NotFoundException:
#         raise HTTPException(status_code=404, detail="Nenhum registro associado a esse plano de treino.")


@ExercisePlanRouter.post("", response_model=ExercisePlan)
def create(exercise_plan_body: ExercisePlanCreate, exercise_plan_service: ExercisePlanService = Depends()):
    exercise_plan = exercise_plan_service.create(exercise_plan_body)
    return exercise_plan


@ExercisePlanRouter.put("", response_model=ExercisePlanWithName)
def update(exercise_plan_body: ExercisePlanUpdate, exercise_plan_service: ExercisePlanService = Depends()):
    try:
        exercise_plan = exercise_plan_service.update(exercise_plan_body)
        return exercise_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@ExercisePlanRouter.delete("/{exercise_plan_id}")
def delete(exercise_plan_id: int, exercise_plan_service: ExercisePlanService = Depends()):
    try:
        exercise_plan_service.delete(exercise_plan_id)
        return {"message": "Registro deletado."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
