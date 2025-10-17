from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.appointment_model import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from .dependency import get_session


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=Appointment)
def insert_appointment(appointment: Appointment, session: Session = Depends(get_session)):
    appointment_repository = AppointmentRepository(session)
    return appointment_repository.insert_appointment(appointment)


@router.get("/", response_model=List[Appointment])
def list_all_appointments(session: Session = Depends(get_session)):
    appointment_repository = AppointmentRepository(session)
    return appointment_repository.list_all_appointments()


@router.get("/{appointment_id}", response_model=Appointment)
def search_appointment_by_id(appointment_id: int, session: Session = Depends(get_session)):
    appointment_repository = AppointmentRepository(session)
    appointment = appointment_repository.search_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: int, appointment_update: dict, session: Session = Depends(get_session)):
    appointment_repository = AppointmentRepository(session)
    try:
        return appointment_repository.update_appointment(appointment_id, appointment_update)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, session: Session = Depends(get_session)):
    appointment_repository = AppointmentRepository(session)
    try:
        appointment_repository.delete_appointment(appointment_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))