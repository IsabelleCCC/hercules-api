from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from business.services.auth import AuthService
from business.services.exercise_done import ExerciseDoneService
from business.services.exceptions import NotFoundException
from core.schemas.exercise_done import ExerciseDone, ExerciseDoneWithName, ExerciseDoneCreate, ExerciseDoneBase

ExerciseDoneRouter = APIRouter(
    prefix='/exercise-done', tags=['exercise-done']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@ExerciseDoneRouter.get("", response_model=List[ExerciseDoneWithName])
def list(workout_done_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, exercise_done_service: ExerciseDoneService = Depends()):
    try:
        exercise_done_list = exercise_done_service.list(workout_done_id, skip, limit)
        return exercise_done_list
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro de exercício feito associado a este treino.")

@ExerciseDoneRouter.post("", response_model=ExerciseDone)
def create(exercise_done_body: ExerciseDoneCreate, exercise_done_service: ExerciseDoneService = Depends()):
    exercise_done = exercise_done_service.create(exercise_done_body)
    return exercise_done

@ExerciseDoneRouter.delete("/{exercise_done_id}")
def delete(exercise_done_id: int, exercise_done_service: ExerciseDoneService = Depends()):
    try:
        exercise_done_service.delete(exercise_done_id)
        return {"message": "Registro deletado."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
