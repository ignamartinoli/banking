from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.repositories.currencies import CurrencyRepository
from app.schemas.accounts import AccountCreate, AccountOut, DepositOut, DepositRequest
from app.services.accounts import AccountService
from app.repositories.accounts import AccountRepository
from app.errors import Forbidden, NotFound
from app.db.models import User

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_account_service() -> AccountService:
    return AccountService(AccountRepository(), CurrencyRepository())


@router.post("", response_model=AccountOut)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    svc: AccountService = Depends(get_account_service),
):
    try:
        return svc.create(
            db,
            owner_id=user.id,
            name=payload.name,
            initial_balance_cents=payload.initial_balance_cents,
            currency_id=payload.currency_id
        )
    except NotFound as e:
        raise HTTPException(404, str(e))


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


@router.post("/{account_id}/deposit", response_model=DepositOut)
def deposit(
    account_id: int,
    payload: DepositRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    svc: AccountService = Depends(get_account_service),
):
    try:
        return svc.deposit(
            db,
            user_id=user.id,
            account_id=account_id,
            amount_cents=payload.amount_cents,
        )
    except NotFound as e:
        raise HTTPException(404, str(e))
    except Forbidden as e:
        raise HTTPException(403, str(e))