from pydantic import BaseModel, Field


class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount_cents: int = Field(gt=0)


class TransferOut(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount_cents: int

    class Config:
        from_attributes: bool = True
