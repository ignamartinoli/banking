from sqlalchemy.orm import Session
from app.db.models import Account
from app.repositories.accounts import AccountRepository
from app.errors import NotFound


class AccountService:
    def __init__(self, accounts: AccountRepository):
        self.accounts: AccountRepository = accounts

    def create(
        self, db: Session, *, owner_id: int, name: str, initial_balance_cents: int
    ) -> Account:
        acc = Account(owner_id=owner_id, name=name, balance_cents=initial_balance_cents)
        _ = self.accounts.add(db, acc)
        db.commit()
        db.refresh(acc)
        return acc

    def list(self, db: Session, *, owner_id: int) -> list[Account]:
        return self.accounts.list_for_owner(db, owner_id)

    def get(self, db: Session, *, owner_id: int, account_id: int) -> Account:
        acc = self.accounts.get_for_owner(db, account_id, owner_id)
        if not acc:
            raise NotFound("Account not found")
        return acc
