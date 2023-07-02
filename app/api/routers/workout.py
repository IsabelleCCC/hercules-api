from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from business.services.auth import AuthService
from business.services.workout import WorkoutService
from business.services.exceptions import NotFoundException, BadRequestException
from core.schemas.workout import WorkoutCreate, WorkoutUpdate, Workout, WorkoutWithExercise

WorkoutRouter = APIRouter(
    prefix='/workout', tags=['workout']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@WorkoutRouter.get("/{workout_id}", response_model=WorkoutWithExercise)
def get(workout_id: int, workout_service: WorkoutService = Depends()):
    try:
        workout = workout_service.get(workout_id)
        return workout
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@WorkoutRouter.get("", response_model=List[WorkoutWithExercise])
def list(user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, workout_service: WorkoutService = Depends()):
    try:
        workout = workout_service.list(user_id, skip, limit)
        return workout
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro associado ao usuário.")


@WorkoutRouter.post("", response_model=List[Workout])
def create(workout_body_list: List[WorkoutCreate], workout_service: WorkoutService = Depends()):
    # try:
    workout = workout_service.create(workout_body_list)
    return workout
    # except BadRequestException:
    #     raise HTTPException(status_code=400, detail="Não foi possível inserir.")


@WorkoutRouter.put("", response_model=WorkoutWithExercise)
def update(workout_body: WorkoutUpdate, workout_service: WorkoutService = Depends()):
    try:
        workout = workout_service.update(workout_body)
        return workout
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@WorkoutRouter.delete("/{workout_id}")
def delete(workout_id: int, workout_service: WorkoutService = Depends()):
    try:
        workout_service.delete(workout_id)
        return {"message": "Registro deletado."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
