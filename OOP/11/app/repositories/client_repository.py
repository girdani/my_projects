from typing import TYPE_CHECKING

from sqlmodel import Session, select

if TYPE_CHECKING:
    from ..models.client_model import Client


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_client(self, client: "Client") -> "Client":
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def list_all_clients(self) -> list["Client"]:
        statement = select(Client)
        results = self.session.exec(statement)
        return results.all()

    def search_client_by_id(self, id: int) -> "Client" | None:
        return self.session.get(Client, id)

    def update_client(self, id: int, kwargs: dict) -> "Client":
        client = self.session.get(Client, id)
        if not client:
            raise ValueError("Could not find client.")

        for key, value in kwargs.items():
            setattr(client, key, value)

        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def delete_client(self, id: int) -> None:
        client = self.session.get(Client, id)
        if not client:
            raise ValueError("Could not find client.")

        self.session.delete(client)
        self.session.commit()