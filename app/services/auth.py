from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.db.models import User
from app.errors import Conflict, Forbidden
from app.repositories.users import UserRepository


class AuthService:
    def __init__(self, users: UserRepository):
        self.users: UserRepository = users

    def register(self, db: Session, *, email: str, password: str) -> str:
        if self.users.get_by_email(db, email):
            raise Conflict("Email already registered")
        user = User(email=email, password_hash=hash_password(password))
        _ = self.users.add(db, user)
        db.commit()
        return create_access_token(subject=email)

    def login(self, db: Session, *, email: str, password: str) -> str:
        user = self.users.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise Forbidden("Bad credentials")
        return create_access_token(subject=email)
