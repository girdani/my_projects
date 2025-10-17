from typing import TYPE_CHECKING

from sqlmodel import Session, select

if TYPE_CHECKING:
    from ..models.service_model import Service


class ServiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_service(self, service: "Service") -> "Service":
        self.session.add(service)
        self.session.commit()
        self.session.refresh(service)
        return service

    def list_all_services(self) -> list["Service"]:
        statement = select(Service)
        results = self.session.exec(statement)
        return results.all()

    def search_service_by_id(self, id: int) -> "Service" | None:
        return self.session.get(Service, id)

    def update_service(self, id: int, kwargs: dict) -> "Service":
        service = self.session.get(Service, id)
        if not service:
            raise ValueError("Could not find service.")

        for key, value in kwargs.items():
            setattr(service, key, value)

        self.session.add(service)
        self.session.commit()
        self.session.refresh(service)
        return service

    def delete_service(self, id: int) -> None:
        service = self.session.get(Service, id)
        if not service:
            raise ValueError("Could not find service.")

        self.session.delete(service)
        self.session.commit()
