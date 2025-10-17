from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository
from .dependency import get_session


router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=Client)
def insert_client(client: Client, session: Session = Depends(get_session)):
    client_repository = ClientRepository(session)
    return client_repository.insert_client(client)


@router.get("/", response_model=List[Client])
def list_all_clients(session: Session = Depends(get_session)):
    client_repository = ClientRepository(session)
    return client_repository.list_all_clients()


@router.get("/{client_id}", response_model=Client)
def search_client_by_id(client_id: int, session: Session = Depends(get_session)):
    client_repository = ClientRepository(session)
    client = client_repository.search_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.patch("/{client_id}", response_model=Client)
def update_client(client_id: int, client_update: dict, session: Session = Depends(get_session)):
    client_repository = ClientRepository(session)
    try:
        return client_repository.update_client(client_id, client_update)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, session: Session = Depends(get_session)):
    client_repository = ClientRepository(session)
    try:
        client_repository.delete_client(client_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))