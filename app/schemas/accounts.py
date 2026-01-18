from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    initial_balance_cents: int = Field(ge=0, default=0)


class AccountOut(BaseModel):
    id: int
    name: str
    balance_cents: int

    class Config:
        from_attributes = True
