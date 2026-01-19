from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.currencies import CurrencyOut
from app.repositories.currencies import CurrencyRepository


router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("", response_model=list[CurrencyOut])
def list_currencies(db: Session = Depends(get_db)):
    return CurrencyRepository().list_all(db)
