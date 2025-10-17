from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from .dependency import get_session


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def insert_user(user: User, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    return user_repository.insert_user(user)


@router.get("/", response_model=List[User])
def list_all_users(session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    return user_repository.list_all_users()


@router.get("/{user_id}", response_model=User)
def search_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    user = user_repository.search_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/by_email", response_model=Optional[User])
def search_user_by_email(email: str = Query(..., description="User email to search"), session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    user = user_repository.search_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: dict, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    try:
        return user_repository.update_user(user_id, user_update)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    try:
        user_repository.delete_user(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))