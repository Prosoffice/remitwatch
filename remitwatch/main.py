from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import Quote
from .pricing import effective_rate, rank_offers, received_amount
from .schemas import Comparison, QuoteIn, QuoteOut


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="RemitWatch", description="Compare GBP→NGN remittance offers after fees.", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/quotes", response_model=QuoteOut, status_code=201)
def record_quote(payload: QuoteIn, session: Session = Depends(get_session)):
    quote = Quote(**payload.model_dump())
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote


def _latest_per_provider(session: Session) -> list[Quote]:
    latest = (
        select(Quote.provider, func.max(Quote.observed_at).label("observed_at")).group_by(Quote.provider).subquery()
    )
    stmt = select(Quote).join(
        latest, (Quote.provider == latest.c.provider) & (Quote.observed_at == latest.c.observed_at)
    )
    return list(session.scalars(stmt))


@app.get("/compare", response_model=list[Comparison])
def compare(
    amount: Decimal = Query(Decimal("100"), gt=0, description="GBP you want to send"),
    session: Session = Depends(get_session),
):
    """Latest offer from each provider, best first, for the amount you want to send."""
    offers = rank_offers(_latest_per_provider(session), amount)
    return [
        Comparison(
            provider=q.provider,
            rate=q.rate,
            fee=q.fee,
            send_amount=amount,
            total_paid=amount + q.fee,
            recipient_gets=received_amount(amount, q.rate),
            effective_rate=effective_rate(amount, q.rate, q.fee),
            observed_at=q.observed_at,
        )
        for q in offers
    ]


@app.get("/history/{provider}", response_model=list[QuoteOut])
def history(provider: str, limit: int = Query(50, le=500), session: Session = Depends(get_session)):
    stmt = select(Quote).where(Quote.provider == provider).order_by(Quote.observed_at.desc()).limit(limit)
    quotes = list(session.scalars(stmt))
    if not quotes:
        raise HTTPException(status_code=404, detail=f"No quotes recorded for {provider}")
    return quotes
