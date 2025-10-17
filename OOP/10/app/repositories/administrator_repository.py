from typing import TYPE_CHECKING
from sqlmodel import Session, select

if TYPE_CHECKING:
    from ..models import Administrator

class AdministratorRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_administrator(self, admin: "Administrator") -> "Administrator":
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin

    def list_all_administrators(self) -> list["Administrator"]:
        statement = select(Administrator)
        results = self.session.exec(statement)
        return results.all()

    def search_administrator_by_id(self, id: int) -> "Administrator":
        admin = self.session.get(Administrator, id)
        if not admin:
            raise ValueError("could not find administrator.")
        
        return admin

    def update_administrator(self, id: int, kwargs: dict) -> "Administrator":
        admin = self.session.get(Administrator, id)
        if not admin:
            raise ValueError("could not find administrator.")

        for key, value in kwargs.items():
            setattr(admin, key, value)

        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)

        return admin

    def delete_administrator(self, id: int) -> None:
        admin = self.session.get(Administrator, id)
        if not admin:
            raise ValueError("could not find administrator.")

        self.session.delete(admin)
        self.session.commit()