from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User


class UserRepository:
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def add(self, db: Session, user: User) -> User:
        db.add(user)
        return user
