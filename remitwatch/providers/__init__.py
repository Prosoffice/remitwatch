"""Rate providers.

A provider knows how to fetch a live GBP→NGN offer from one remittance service.
None ship yet: quotes are recorded manually through the API until each provider
is implemented (see ROADMAP.md).
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class Offer:
    provider: str
    rate: Decimal
    fee: Decimal


class Provider(Protocol):
    name: str

    def fetch(self, send_amount: Decimal) -> Offer: ...


class StaticProvider:
    """Returns a fixed offer. Useful for tests and for services without a public rate page."""

    def __init__(self, name: str, rate: Decimal, fee: Decimal = Decimal("0")):
        self.name = name
        self._offer = Offer(provider=name, rate=rate, fee=fee)

    def fetch(self, send_amount: Decimal) -> Offer:
        return self._offer
