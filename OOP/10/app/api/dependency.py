from typing import Generator
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///database.db")

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session