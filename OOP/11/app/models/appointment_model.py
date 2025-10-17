from typing import Optional, TYPE_CHECKING
from datetime import datetime

from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .client_model import Client
    from .service_model import Service


class Appointment(SQLModel, table=True):
    __tablename__ = "appointments"

    # --- Identification & Foreign Keys ---
    id: Optional[int] = Field(default=None, primary_key=True)
    clientId: int = Field(foreign_key="clients.id")  # Foreign key added
    serviceId: int = Field(foreign_key="services.id")  # Foreign key added

    # --- Main Fields ---
    date_hour: datetime
    description: str
    price: float

    # --- Relationships ---
    client: "Client" = Relationship(back_populates="appointments")
    service: "Service" = Relationship(back_populates="appointments")

    @field_validator("description", mode="after")
    def _validate_description(cls, description: str) -> str:
        if not description.strip():
            raise ValueError("description cannot be empty.")
        return description

    @field_validator("price", mode="after")
    def _validate_price(cls, price: float) -> float:
        if price < 0:
            raise ValueError("price cannot be negative.")
        if not price == round(price, 2):
            raise ValueError("price cannot contain more than two decimal places.")
        return price

    class Config:
        validate_assignment = True
