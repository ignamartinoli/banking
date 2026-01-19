from pydantic import BaseModel, ConfigDict, Field


class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount_cents: int = Field(gt=0)


class TransferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_account_id: int
    to_account_id: int
    amount_cents: int
