# Roadmap

## Getting rates automatically
- [ ] Provider adapters for the services I use, starting with public rate pages and calculators, respecting each site's terms
- [ ] Scheduled fetching (every few hours) with retries and a record of failures
- [ ] Mark stale quotes and leave them out of comparisons
- [ ] Mid-market reference rate to show each provider's markup

## Alerts
- [ ] Alert rules: "tell me when the effective rate for £200 goes above X"
- [ ] Notifications by email first, then Telegram or WhatsApp
- [ ] Daily summary of the best offer

## Comparisons
- [ ] Fee tiers that depend on amount (many services charge differently above thresholds)
- [ ] Delivery method (bank transfer vs mobile money) and transfer speed per offer
- [ ] Other corridors (EUR→NGN, GBP→GHS) once GBP→NGN is solid

## Frontend
- [ ] Simple web page: enter an amount, see the ranked offers
- [ ] Rate history chart per provider

## Engineering
- [ ] Alembic migrations instead of `create_all`
- [ ] GitHub Actions: tests and linting on every push
- [ ] Dockerfile and a small deployment guide
