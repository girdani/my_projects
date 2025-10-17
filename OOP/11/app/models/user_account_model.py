from typing import Optional, TYPE_CHECKING
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .client_model import Client
    from .administrator_model import Administrator


class UserAccount(SQLModel, table=True):
    __tablename__ = "users_accounts"

    # --- Identification & Foreign Keys ---
    id: Optional[int] = Field(default=None, primary_key=True)

    # --- Main Fields ---
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    phone: str

    # --- Relationships ---
    client: Optional["Client"] = Relationship(back_populates="user")
    administrator: Optional["Administrator"] = Relationship(back_populates="user")

    # --- Validators ---
    @field_validator("name", mode="after")
    def _validate_name(cls, name: str) -> str:
        if not name.strip():
            raise ValueError("name cannot be empty.")
        return name

    @field_validator("email", mode="after")
    def _validate_email(cls, email: str) -> str:
        if not email.strip():
            raise ValueError("email cannot be empty.")
        return email

    @field_validator("password", mode="after")
    def _validate_password(cls, password: str) -> str:
        if not password.strip():
            raise ValueError("password cannot be empty.")
        return password

    @field_validator("phone", mode="after")
    def _validate_phone(cls, phone: str) -> str:
        if not phone.strip():
            raise ValueError("phone cannot be empty.")
        return phone

    class Config:
        validate_assignment = True