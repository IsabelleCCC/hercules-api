from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from business.services.auth import AuthService
from business.services.exercise import ExerciseService
from business.services.exceptions import NotFoundException
from core.schemas.exercise import ExerciseCreate, ExerciseUpdate, Exercise

ExerciseRouter = APIRouter(
    prefix='/exercise', tags=['exercise'], dependencies=[Depends(AuthService.get_current_user)]
)

@ExerciseRouter.get("/{exercise_id}", response_model=Exercise, summary='Get exercise by id')
def get(exercise_id: int, exercise_service: ExerciseService = Depends()):
    try:
        exercise = exercise_service.get(exercise_id)
        return exercise
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail='Exercício não encontrado.')


@ExerciseRouter.get("", response_model=List[Exercise], summary='List exercises')
def list(skip: Optional[int] = 0, limit: Optional[int] = 10, exercise_service: ExerciseService = Depends()):
    try:
        exercises = exercise_service.list(skip, limit)
        return exercises
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum exercício encontrado.")


@ExerciseRouter.post("", response_model=Exercise, summary='Create exercise')
def create(exercise_body: ExerciseCreate, exercise_service: ExerciseService = Depends()):
    exercise = exercise_service.create(exercise_body)
    return exercise


@ExerciseRouter.put("", response_model=Exercise, summary='Update exercise')
def update(exercise_body: ExerciseUpdate, exercise_service: ExerciseService = Depends()):
    try:
        exercise = exercise_service.update(exercise_body)
        return exercise
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")



@ExerciseRouter.delete("/{exercise_id}", summary='Delete exercise')
def delete(exercise_id: int, exercise_service: ExerciseService = Depends()):
    try:
        exercise_service.delete(exercise_id)
        return {"message": "Exercício deletado."}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")
