from typing import TYPE_CHECKING
from sqlmodel import Session, select

if TYPE_CHECKING:
    from ..models import Administrator


class AdministratorRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_administrator(self, administrator: "Administrator") -> "Administrator":
        self.session.add(administrator)
        self.session.commit()
        self.session.refresh(administrator)
        return administrator

    def list_all_administrators(self) -> list["Administrator"]:
        statement = select(Administrator)
        results = self.session.exec(statement)
        return results.all()

    def search_administrator_by_id(self, id: int) -> "Administrator" | None:
        return self.session.get(Administrator, id)

    def update_administrator(self, id: int, kwargs: dict) -> "Administrator":
        administrator = self.session.get(Administrator, id)
        if not administrator:
            raise ValueError("Could not find administrator.")

        for key, value in kwargs.items():
            setattr(administrator, key, value)

        self.session.add(administrator)
        self.session.commit()
        self.session.refresh(administrator)
        return administrator

    def delete_administrator(self, id: int) -> None:
        administrator = self.session.get(Administrator, id)
        if not administrator:
            raise ValueError("Could not find administrator.")

        self.session.delete(administrator)
        self.session.commit()