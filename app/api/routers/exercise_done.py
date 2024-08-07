from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from business.services.muscle_group_by_date import MuscleGroupByDateService
from core.schemas.muscle_group_by_date import MuscleGroupByDate
from business.services.auth import AuthService
from business.services.exercise_done import ExerciseDoneService
from business.services.exceptions import NotFoundException
from core.schemas.exercise_done import ExerciseDone, ExerciseDoneByUser, ExerciseDoneWithName, ExerciseDoneCreate, ExerciseDoneBase, ExerciseDoneWithPagination

ExerciseDoneRouter = APIRouter(
    prefix='/exercise-done', tags=['exercise-done']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@ExerciseDoneRouter.get("/{workout_done_id}", response_model=List[ExerciseDoneWithName])
def list_by_workout_done(workout_done_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, exercise_done_service: ExerciseDoneService = Depends()):
    try:
        exercise_done_list = exercise_done_service.list_by_workout_done(workout_done_id, skip, limit)
        return exercise_done_list
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro de exercício feito associado a este treino.")


@ExerciseDoneRouter.get("/user-id/{user_id}", response_model=ExerciseDoneWithPagination)
def list_by_user_id(user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, exercise_done_service: ExerciseDoneService = Depends()):
    try:
        exercise_done_list = exercise_done_service.list_by_user_id(user_id, skip, limit)
        return exercise_done_list
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro de exercício feito associado a este treino.")


@ExerciseDoneRouter.get("/muscle-group-by-date/{user_id}", response_model=List[MuscleGroupByDate])
def list_muscle_group_by_date(user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 365, muscle_group_by_date_service: MuscleGroupByDateService = Depends()):
    try:
        muscle_group_by_date = muscle_group_by_date_service.list(user_id, skip, limit)
        return muscle_group_by_date
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado.")


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
