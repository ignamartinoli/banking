from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Currency


class CurrencyRepository:
    def list_all(self, db: Session) -> list[Currency]:
        return list(db.execute(select(Currency).order_by(Currency.code)).scalars().all())
    

    def get_by_id(self, db: Session, currency_id: int) -> Currency | None:
        return db.execute(select(Currency).where(Currency.id == currency_id)).scalar_one_or_none()
    
    
    def get_by_code(self, db: Session, code: str) -> Currency | None:
        return db.execute(select(Currency).where(Currency.code == code)).scalar_one_or_none()