from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    initial_balance_cents: int = Field(ge=0, default=0)
    currency_id: int | None = None


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    currency_id: int
    balance_cents: int


class DepositRequest(BaseModel):
    amount_cents: int = Field(gt=0)


class DepositOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    balance_cents: int