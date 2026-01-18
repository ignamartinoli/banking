from sqlalchemy.orm import Session
from app.db.models import Transfer
from app.repositories.accounts import AccountRepository
from app.repositories.transfers import TransferRepository
from app.errors import NotFound, Forbidden, InsufficientFunds, Conflict


class TransferService:
    def __init__(self, accounts: AccountRepository, transfers: TransferRepository):
        self.accounts: AccountRepository = accounts
        self.transfers: TransferRepository = transfers

    def create_transfer(
        self,
        db: Session,
        *,
        user_id: int,
        from_account_id: int,
        to_account_id: int,
        amount_cents: int,
    ) -> Transfer:
        if from_account_id == to_account_id:
            raise Conflict("from_account_id and to_account_id must differ")

        # Transaction boundary lives in service
        with db.begin_nested():
            from_acc = self.accounts.get_for_update(db, from_account_id)
            to_acc = self.accounts.get_for_update(db, to_account_id)

            if not from_acc or not to_acc:
                raise NotFound("Account not found")
            if from_acc.owner_id != user_id:
                raise Forbidden("Not your source account")
            if from_acc.balance_cents < amount_cents:
                raise InsufficientFunds("Insufficient funds")

            from_acc.balance_cents -= amount_cents
            to_acc.balance_cents += amount_cents

            tx = Transfer(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount_cents=amount_cents,
            )
            self.transfers.add(db, tx)

        db.refresh(tx)
        return tx
