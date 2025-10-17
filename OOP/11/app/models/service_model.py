from typing import Optional, TYPE_CHECKING
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .appointment_model import Appointment


class Service(SQLModel, table=True):
    __tablename__ = "services"

    # --- Identification & Foreign Keys ---
    id: Optional[int] = Field(default=None, primary_key=True)

    # --- Main Fields ---
    name: str
    standard_description: str
    standard_price: float

    # --- Relationships ---
    appointments: list["Appointment"] = Relationship(back_populates="service")

    @field_validator("name", mode="after")
    def _validate_name(cls, name: str) -> str:
        if not name.strip():
            raise ValueError("name cannot be empty.")
        return name

    @field_validator("standard_description", mode="after")
    def _validate_standard_description(cls, desc: str) -> str:
        if not desc.strip():
            raise ValueError("standard description cannot be empty.")
        return desc

    @field_validator("standard_price", mode="after")
    def _validate_standard_price(cls, price: float) -> float:
        if price < 0:
            raise ValueError("standard price cannot be negative.")
        if not price == round(price, 2):
            raise ValueError("standard price cannot contain more than two decimal places.")
        return price

    class Config:
        validate_assignment = True