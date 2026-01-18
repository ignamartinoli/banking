from sqlalchemy.orm import Session
from app.db.models import Transfer


class TransferRepository:
    def add(self, db: Session, tx: Transfer) -> Transfer:
        db.add(tx)
        return tx
