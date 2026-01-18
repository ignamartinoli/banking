from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import UserCreate, Token
from app.services.auth import AuthService
from app.repositories.users import UserRepository
from app.errors import Conflict, Forbidden

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService(UserRepository())


@router.post("/register", response_model=Token)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
    svc: AuthService = Depends(get_auth_service),
):
    try:
        token = svc.register(db, email=payload.email, password=payload.password)
        return {"access_token": token}
    except Conflict as e:
        raise HTTPException(400, str(e))


@router.post("/login", response_model=Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    svc: AuthService = Depends(get_auth_service),
):
    try:
        token = svc.login(db, email=username, password=password)
        return {"access_token": token}
    except Forbidden as e:
        raise HTTPException(401, str(e))
