from typing import Optional, TYPE_CHECKING
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .client_model import Client
    from .administrator_model import Administrator


class User(SQLModel, table=True):
    __tablename__ = "users"

    # --- Identification ---
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)

    # --- Main Fields ---
    name: str
    phone: str

    # --- Relationships ---
    client: Optional["Client"] = Relationship(back_populates="user")
    administrator: Optional["Administrator"] = Relationship(back_populates="user")

    @field_validator("name", mode="after")
    def _validate_name(cls, name: str) -> str:
        if not name.strip():
            raise ValueError("name cannot be empty.")
        return name

    @field_validator("phone", mode="after")
    def _validate_phone(cls, phone: str) -> str:
        if not phone.strip():
            raise ValueError("phone cannot be empty.")
        return phone

    @field_validator("email", mode="after")
    def _validate_email(cls, email: str) -> str:
        if not email.strip():
            raise ValueError("email cannot be empty.")
        return email

    class Config:
        validate_assignment = True