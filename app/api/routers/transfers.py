from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.transfers import TransferCreate, TransferOut
from app.services.transfers import TransferService
from app.repositories.accounts import AccountRepository
from app.repositories.transfers import TransferRepository
from app.db.models import User

router = APIRouter(prefix="/transfers", tags=["transfers"])

def get_transfer_service() -> TransferService:
    return TransferService(AccountRepository(), TransferRepository())

@router.post("", response_model=TransferOut)
def create_transfer(
    payload: TransferCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    svc: TransferService = Depends(get_transfer_service),
):
    return svc.create_transfer(
        db,
        user_id=user.id,
        from_account_id=payload.from_account_id,
        to_account_id=payload.to_account_id,
        amount_cents=payload.amount_cents,
    )
