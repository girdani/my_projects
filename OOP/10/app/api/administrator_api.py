from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.administrator_model import Administrator
from app.repositories.administrator_repository import AdministratorRepository
from .dependency import get_session


router = APIRouter(prefix="/administrators", tags=["administrators"])


@router.post("/", response_model=Administrator)
def insert_administrator(administrator: Administrator, session: Session = Depends(get_session)):
    administrator_repository = AdministratorRepository(session)
    return administrator_repository.insert_administrator(administrator)


@router.get("/", response_model=List[Administrator])
def list_all_administrators(session: Session = Depends(get_session)):
    administrator_repository = AdministratorRepository(session)
    return administrator_repository.list_all_administrators()


@router.get("/{administrator_id}", response_model=Administrator)
def search_administrator_by_id(administrator_id: int, session: Session = Depends(get_session)):
    administrator_repository = AdministratorRepository(session)
    administrator = administrator_repository.search_administrator_by_id(administrator_id)
    if not administrator:
        raise HTTPException(status_code=404, detail="Administrator not found")
    return administrator


@router.patch("/{administrator_id}", response_model=Administrator)
def update_administrator(administrator_id: int, administrator_update: dict, session: Session = Depends(get_session)):
    administrator_repository = AdministratorRepository(session)
    try:
        return administrator_repository.update_administrator(administrator_id, administrator_update)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{administrator_id}", status_code=204)
def delete_administrator(administrator_id: int, session: Session = Depends(get_session)):
    administrator_repository = AdministratorRepository(session)
    try:
        administrator_repository.delete_administrator(administrator_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))