from typing import Optional, List, Any

from sqlmodel import Session, select

from ..models.user_account_model import UserAccount


class UserAccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_user(self, user: UserAccount) -> UserAccount:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def list_all_users(self) -> List[UserAccount]:
        statement = select(UserAccount)
        results = self.session.exec(statement)
        return results.all()

    def search_user_by_id(self, id: int) -> UserAccount:
        return self.session.get(UserAccount, id)

    def search_user_by_email(self, email: str) -> UserAccount | None:
        return self.session.exec(
            select(UserAccount).where(UserAccount.email == email)
        ).first()

    def update_user(self, id: int, updated_user_account: UserAccount) -> UserAccount:
        user_account = self.session.get(UserAccount, id)
        if not user_account:
            raise ValueError("Could not find user.")

        update_data = updated_user_account.model_dump(exclude_unset=True, exclude={"id"})

        for key, value in update_data.items():
            setattr(user_account, key, value)

        self.session.add(user_account)
        self.session.commit()
        self.session.refresh(user_account)
        return user_account

    def delete_user(self, id: int) -> None:
        user = self.session.get(UserAccount, id)
        if not user:
            raise ValueError("Could not find user.")

        self.session.delete(user)
        self.session.commit()