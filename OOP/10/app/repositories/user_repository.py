from sqlmodel import Session, select
from ..models import User  


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def insert_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def list_all_users(self) -> list[User]:
        statement = select(User)
        results = self.session.exec(statement)
        return results.all()
    
    def search_user_by_id(self, id: int) -> User | None:
        return self.session.get(User, id)

    def search_user_by_email(self, email: str) -> User | None:
        return self.session.exec(
            select(User).where(User.email == email)
        ).first()
    
    def update_user(self, id: int, kwargs: dict) -> User | None:
        user = self.session.get(User, id)
        if not user:
            return ValueError("could not find user.")
        
        for key, value in kwargs.items():
            setattr(user, key, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete_user(self, id: int):
        user = self.session.get(User, id)
        if not user:
            return ValueError("could not find user.")
        
        self.session.delete(user)
        self.session.commit()