from decimal import Decimal

import pytest

from remitwatch.pricing import effective_rate, rank_offers, received_amount
from remitwatch.providers import StaticProvider


def test_received_amount():
    assert received_amount(Decimal("100"), Decimal("2000")) == Decimal("200000.00")


def test_effective_rate_accounts_for_fee():
    # £100 at 2000 with a £2 fee: recipient gets 200,000 for £102 paid
    assert effective_rate(Decimal("100"), Decimal("2000"), Decimal("2")) == Decimal("1960.7843")


def test_effective_rate_rejects_non_positive_total():
    with pytest.raises(ValueError):
        effective_rate(Decimal("0"), Decimal("2000"), Decimal("0"))


def test_lower_headline_rate_can_win_after_fees():
    cheap_fee = StaticProvider("A", rate=Decimal("1990"), fee=Decimal("0")).fetch(Decimal("50"))
    high_rate = StaticProvider("B", rate=Decimal("2020"), fee=Decimal("2.99")).fetch(Decimal("50"))
    ranked = rank_offers([high_rate, cheap_fee], Decimal("50"))
    assert [o.provider for o in ranked] == ["A", "B"]
