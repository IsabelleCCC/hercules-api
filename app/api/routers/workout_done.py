from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from business.services.auth import AuthService
from business.services.workout_done import WorkoutDoneService
from business.services.exceptions import NotFoundException, BadRequestException
from core.schemas.workout_done import WorkoutDoneCreate, WorkoutDoneUpdate, WorkoutDone, WorkoutDoneWithName

WorkoutDoneRouter = APIRouter(
    prefix='/workout-done', tags=['workout-done']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@WorkoutDoneRouter.get("/{workout_done_id}", response_model=WorkoutDone)
def get(workout_done_id: int, workout_done_service: WorkoutDoneService = Depends()):
    try:
        workout_done = workout_done_service.get(workout_done_id)
        return workout_done
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@WorkoutDoneRouter.get("", response_model=List[WorkoutDoneWithName])
def list(user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, workout_done_service: WorkoutDoneService = Depends()):
    try:
        workout_done = workout_done_service.list(user_id, skip, limit)
        return workout_done
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro associado ao usuário.")


@WorkoutDoneRouter.post("", response_model=WorkoutDone)
def create(workout_done_body: WorkoutDoneCreate, workout_done_service: WorkoutDoneService = Depends()):
    workout_done = workout_done_service.create(workout_done_body)
    return workout_done

@WorkoutDoneRouter.put("", response_model=WorkoutDone)
def update(workout_body: WorkoutDoneUpdate, workout_done_service: WorkoutDoneService = Depends()):
    try:
        workout_done = workout_done_service.update(workout_body)
        return workout_done
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")


@WorkoutDoneRouter.delete("/{workout_done_id}")
def delete(workout_done_id: int, workout_done_service: WorkoutDoneService = Depends()):
    try:
        workout_done_service.delete(workout_done_id)
        return {"message": "Registro deletado."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
