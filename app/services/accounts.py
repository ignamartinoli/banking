from sqlalchemy.orm import Session
from app.db.models import Account
from app.repositories.accounts import AccountRepository
from app.errors import Forbidden, NotFound
from app.repositories.currencies import CurrencyRepository


class AccountService:
    def __init__(self, accounts: AccountRepository, currencies: CurrencyRepository):
        self.accounts: AccountRepository = accounts
        self.currencies: CurrencyRepository = currencies

    def create(
        self,
        db: Session,
        *,
        owner_id: int,
        name: str,
        initial_balance_cents: int,
        currency_id: int
    ) -> Account:
        if currency_id is None:
            ars = self.currencies.get_by_code(db, "ARS")
            if not ars:
                raise NotFound("Default currency ARS not found")
            currency_id = ars.id
        else:
            currency = self.currencies.get_by_id(db, currency_id)
            if not currency:
                raise NotFound("Currency not found")

        acc = Account(owner_id=owner_id, name=name, balance_cents=initial_balance_cents, currency_id=currency_id)
        _ = self.accounts.add(db, acc)
        db.flush()
        db.refresh(acc)
        return acc

    def list(self, db: Session, *, owner_id: int) -> list[Account]:
        return self.accounts.list_for_owner(db, owner_id)

    def get(self, db: Session, *, owner_id: int, account_id: int) -> Account:
        acc = self.accounts.get_for_owner(db, account_id, owner_id)
        if not acc:
            raise NotFound("Account not found")
        return acc

    def deposit(
        self,
        db: Session,
        *,
        user_id: int,
        account_id: int,
        amount_cents: int,
    ) -> Account:
        with db.begin_nested():
            acc = self.accounts.get_for_update(db, account_id)
            if not acc:
                raise NotFound("Account not found")
            if acc.owner_id != user_id:
                raise Forbidden("Not your account")

            acc.balance_cents += amount_cents
    
        db.refresh(acc)
        return acc
