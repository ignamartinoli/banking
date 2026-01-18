from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Account


class AccountRepository:
    def list_for_owner(self, db: Session, owner_id: int) -> list[Account]:
        return list(
            db.execute(select(Account).where(Account.owner_id == owner_id))
            .scalars()
            .all()
        )

    def get_for_owner(
        self, db: Session, account_id: int, owner_id: int
    ) -> Account | None:
        return db.execute(
            select(Account).where(
                Account.id == account_id, Account.owner_id == owner_id
            )
        ).scalar_one_or_none()

    def get_for_update(self, db: Session, account_id: int) -> Account | None:
        # Row lock to protect concurrent transfers (Postgres)
        stmt = select(Account).where(Account.id == account_id).with_for_update()
        return db.execute(stmt).scalar_one_or_none()

    def add(self, db: Session, account: Account) -> Account:
        db.add(account)
        return account
