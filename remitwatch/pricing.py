"""Comparing offers: what does the recipient actually get for what I pay?"""

from decimal import ROUND_HALF_UP, Decimal


def received_amount(send_amount: Decimal, rate: Decimal) -> Decimal:
    return (send_amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def effective_rate(send_amount: Decimal, rate: Decimal, fee: Decimal) -> Decimal:
    """Rate after fees: what the recipient gets per pound actually paid (amount + fee)."""
    total_paid = send_amount + fee
    if total_paid <= 0:
        raise ValueError("send amount plus fee must be positive")
    return (received_amount(send_amount, rate) / total_paid).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def rank_offers(offers, send_amount: Decimal):
    """Sort offers best-first by effective rate. Each offer needs `rate` and `fee` attributes."""
    return sorted(offers, key=lambda o: effective_rate(send_amount, o.rate, o.fee), reverse=True)
