from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..core import get_session
from ..models import UserAccount
from ..repositories import UserAccountRepository


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserAccount)
def create_user(user: UserAccount, session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    return user_account_repository.insert_user(user)


@router.get("/", response_model=List[UserAccount])
def list_users(session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    return user_account_repository.list_all_users()


@router.get("/{user_id}", response_model=UserAccount)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    user = user_account_repository.search_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/by-email/", response_model=UserAccount)
def get_user_by_email(email: str, session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    user = user_account_repository.search_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserAccount)
def update_user(user_id: int, updated_user: UserAccount, session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    updated = user_account_repository.update_user(user_id, updated_user)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    deleted = user_account_repository.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return


@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    user_account_repository = UserAccountRepository(session)
    user = user_account_repository.search_user_by_email(email)
    if not user or user.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or email")
    return True
