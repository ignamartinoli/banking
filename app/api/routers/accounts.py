from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.accounts import AccountCreate, AccountOut
from app.services.accounts import AccountService
from app.repositories.accounts import AccountRepository
from app.errors import NotFound
from app.db.models import User

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_account_service() -> AccountService:
    return AccountService(AccountRepository())


@router.post("", response_model=AccountOut)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    svc: AccountService = Depends(get_account_service),
):
    acc = svc.create(
        db,
        owner_id=user.id,
        name=payload.name,
        initial_balance_cents=payload.initial_balance_cents,
    )
    return acc


@router.get("", response_model=list[AccountOut])
def list_accounts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    svc: AccountService = Depends(get_account_service),
):
    return svc.list(db, owner_id=user.id)


@router.get("/{account_id}", response_model=AccountOut)
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    svc: AccountService = Depends(get_account_service),
):
    try:
        return svc.get(db, owner_id=user.id, account_id=account_id)
    except NotFound as e:
        raise HTTPException(404, str(e))
