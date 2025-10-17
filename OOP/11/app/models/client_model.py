from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user_account_model import UserAccount
    from .appointment_model import Appointment


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    # --- Identification & Foreign Keys ---
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users_accounts.id")

    # --- Relationships ---
    user_account: "UserAccount" = Relationship(back_populates="client")
    appointments: list["Appointment"] = Relationship(back_populates="client")

    class Config:
        validate_assignment = True