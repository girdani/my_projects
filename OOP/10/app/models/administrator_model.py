from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user_model import User


class Administrator(SQLModel, table=True):
    __tablename__ = "administrators"

    # --- Identification & Foreign Keys ---
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int

    # --- Relationships ---
    user: "User" = Relationship(back_populates="administrator")

    class Config:
        validate_assignment = True