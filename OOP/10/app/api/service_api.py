from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.service_model import Service
from app.repositories.service_repository import ServiceRepository
from .dependency import get_session


router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=Service)
def insert_service(service: Service, session: Session = Depends(get_session)):
    service_repository = ServiceRepository(session)
    return service_repository.insert_service(service)


@router.get("/", response_model=List[Service])
def list_all_services(session: Session = Depends(get_session)):
    service_repository = ServiceRepository(session)
    return service_repository.list_all_services()


@router.get("/{service_id}", response_model=Service)
def search_service_by_id(service_id: int, session: Session = Depends(get_session)):
    service_repository = ServiceRepository(session)
    service = service_repository.search_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.patch("/{service_id}", response_model=Service)
def update_service(service_id: int, service_update: dict, session: Session = Depends(get_session)):
    service_repository = ServiceRepository(session)
    try:
        return service_repository.update_service(service_id, service_update)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int, session: Session = Depends(get_session)):
    service_repository = ServiceRepository(session)
    try:
        service_repository.delete_service(service_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))