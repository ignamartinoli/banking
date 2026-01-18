from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.transfers import TransferCreate, TransferOut
from app.services.transfers import TransferService
from app.repositories.accounts import AccountRepository
from app.repositories.transfers import TransferRepository
from app.errors import NotFound, Forbidden, InsufficientFunds, Conflict
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
    try:
        return svc.create_transfer(
            db,
            user_id=user.id,
            from_account_id=payload.from_account_id,
            to_account_id=payload.to_account_id,
            amount_cents=payload.amount_cents,
        )
    except NotFound as e:
        raise HTTPException(404, str(e))
    except Forbidden as e:
        raise HTTPException(403, str(e))
    except InsufficientFunds as e:
        raise HTTPException(400, str(e))
    except Conflict as e:
        raise HTTPException(400, str(e))
