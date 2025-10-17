from typing import TYPE_CHECKING

from sqlmodel import Session, select

if TYPE_CHECKING:
    from ..models.appointment_model import Appointment


class AppointmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_appointment(self, appointment: "Appointment") -> "Appointment":
        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return appointment

    def list_all_appointments(self) -> list["Appointment"]:
        statement = select(Appointment)
        results = self.session.exec(statement)
        return results.all()

    def search_appointment_by_id(self, id: int) -> "Appointment" | None:
        return self.session.get(Appointment, id)

    def update_appointment(self, id: int, kwargs: dict) -> "Appointment":
        appointment = self.session.get(Appointment, id)
        if not appointment:
            raise ValueError("Could not find appointment.")

        for key, value in kwargs.items():
            setattr(appointment, key, value)

        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return appointment

    def delete_appointment(self, id: int) -> None:
        appointment = self.session.get(Appointment, id)
        if not appointment:
            raise ValueError("Could not find appointment.")

        self.session.delete(appointment)
        self.session.commit()