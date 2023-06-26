from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from business.services.auth import AuthService
from business.services.fitness_test import FitnessTestService
from business.services.exceptions import NotFoundException
from core.schemas.fitness_test import FitnessTestCreate, FitnessTestUpdate, FitnessTest

FitnessTestRouter = APIRouter(
    prefix='/fitness-test', tags=['fitness-test']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@FitnessTestRouter.get("/{fitness_test_id}", response_model=FitnessTest, summary='Get fitness test by id')
def get(fitness_test_id: int, fitness_test_service: FitnessTestService = Depends()):
    try:
        fitness_test = fitness_test_service.get(fitness_test_id)
        return fitness_test
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail='Avaliação física não encontrada.')


@FitnessTestRouter.get("", response_model=List[FitnessTest], summary='List fitness test by user id')
def list(user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, fitness_test_service: FitnessTestService = Depends()):
    try:
        fitness_test_list = fitness_test_service.list(user_id, skip, limit)
        return fitness_test_list
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhuma avaliação física associada a esse usuário.")


@FitnessTestRouter.post("", response_model=FitnessTest, summary='Create fitness test')
def create(fitness_test_body: FitnessTestCreate, fitness_test_service: FitnessTestService = Depends()):
    fitness_test = fitness_test_service.create(fitness_test_body)
    return fitness_test


@FitnessTestRouter.put("", response_model=FitnessTest, summary='Update fitness test')
def update(fitness_test_body: FitnessTestUpdate, fitness_test_service: FitnessTestService = Depends()):
    try:
        fitness_test = fitness_test_service.update(fitness_test_body)
        return fitness_test
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail="Avaliação física não encontrada.")



@FitnessTestRouter.delete("/{fitness_test_id}", summary='Delete fitness test')
def delete(fitness_test_id: int, fitness_test_service: FitnessTestService = Depends()):
    try:
        fitness_test_service.delete(fitness_test_id)
        return {"message": "Avaliação física deletada."}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail="Avaliação física não encontrada.")
