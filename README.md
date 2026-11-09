# RemitWatch

Find out which service actually gets the most naira to your family for the pounds you pay.

Remittance apps advertise headline GBP→NGN rates, but fees change the picture: a slightly lower rate with no fee can beat a better rate with a £2.99 fee, especially on small transfers. RemitWatch records offers from different services and ranks them by **effective rate**, meaning naira received per pound actually paid.

I send money home regularly and got tired of checking three apps every time. This is my tool for that.

## What it does today

- Record a provider's offer (rate and fee) through the API
- `GET /compare?amount=100`: latest offer from each provider, ranked by effective rate, with what the recipient gets
- `GET /history/{provider}`: past offers from one provider
- Interactive API docs at `/docs`

Offers are entered manually for now. Automatic fetching per provider is next on the [roadmap](ROADMAP.md).

## Built with

Python 3.12+, FastAPI, SQLAlchemy 2, Pydantic 2. SQLite by default (any SQLAlchemy URL via `REMITWATCH_DATABASE_URL`).

## Running it locally

```bash
git clone https://github.com/Prosoffice/remitwatch.git
cd remitwatch
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn remitwatch.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

Example:

```bash
curl -X POST localhost:8000/quotes -H 'content-type: application/json' \
  -d '{"provider": "Service A", "rate": "1985", "fee": "0"}'
curl -X POST localhost:8000/quotes -H 'content-type: application/json' \
  -d '{"provider": "Service B", "rate": "2010", "fee": "2.99"}'
curl 'localhost:8000/compare?amount=50'
```

## How the ranking works

`effective rate = (amount × rate) ÷ (amount + fee)`

For £50, Service A at 1,985 with no fee gives ₦99,250 for £50 (effective rate 1,985). Service B at 2,010 with a £2.99 fee gives ₦100,500 for £52.99 (effective rate about 1,897). A wins.

## Tests

```bash
pytest
```

## Licence

MIT. See [LICENSE](LICENSE).
