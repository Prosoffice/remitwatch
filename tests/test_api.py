import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from remitwatch.db import Base, get_session
from remitwatch.main import app


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)

    def override():
        session = TestSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_compare_ranks_latest_offer_per_provider(client):
    client.post("/quotes", json={"provider": "Alpha", "rate": "1980", "fee": "0"})
    client.post("/quotes", json={"provider": "Beta", "rate": "2010", "fee": "1.99"})
    client.post("/quotes", json={"provider": "Alpha", "rate": "2000", "fee": "0"})  # newer Alpha quote

    rows = client.get("/compare", params={"amount": "100"}).json()
    assert [r["provider"] for r in rows] == ["Alpha", "Beta"]
    assert rows[0]["recipient_gets"] == "200000.00"


def test_history_404_for_unknown_provider(client):
    assert client.get("/history/Nobody").status_code == 404


def test_rejects_invalid_quote(client):
    assert client.post("/quotes", json={"provider": "X", "rate": "-1"}).status_code == 422
