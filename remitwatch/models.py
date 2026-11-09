from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Quote(Base):
    """One provider's offer at a point in time: send GBP, recipient gets NGN."""

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), index=True)
    send_currency: Mapped[str] = mapped_column(String(3), default="GBP")
    receive_currency: Mapped[str] = mapped_column(String(3), default="NGN")
    rate: Mapped[Decimal] = mapped_column(Numeric(14, 4), doc="Units of receive currency per 1 send currency")
    fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"), doc="Fee in send currency")
    source: Mapped[str] = mapped_column(String(20), default="manual")
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
