from pydantic import BaseModel, ConfigDict


class CurrencyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str