from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user_model import User
    from .appointment_model import Appointment


class Client(SQLModel, table=True):
    __tablename__ = "clients"
    
    # --- Identification & Foreign Keys ---
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int

    # --- Relationships ---
    user: "User" = Relationship(back_populates="clients")
    appointments: list["Appointment"] = Relationship(back_populates="client")

    class CONFIG:
        validate_assignment = True