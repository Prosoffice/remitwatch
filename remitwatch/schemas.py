from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class QuoteIn(BaseModel):
    provider: str = Field(min_length=1, max_length=50, examples=["Taptap Send"])
    rate: Decimal = Field(gt=0, description="NGN per 1 GBP")
    fee: Decimal = Field(default=Decimal("0"), ge=0, description="Fee in GBP")
    source: str = "manual"


class QuoteOut(QuoteIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    send_currency: str
    receive_currency: str
    observed_at: datetime


class Comparison(BaseModel):
    provider: str
    rate: Decimal
    fee: Decimal
    send_amount: Decimal
    total_paid: Decimal
    recipient_gets: Decimal
    effective_rate: Decimal
    observed_at: datetime
