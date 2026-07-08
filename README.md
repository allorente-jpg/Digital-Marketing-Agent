# Digital Marketing Agent

A starter project for a digital marketing agent app, adapted from the Business Online suite.

## What this project contains

- `backend/` — FastAPI backend for user, customer, invoice, and workflow management
- `backend/app/` — application code and domain models
- `backend/requirements.txt` — package list

## Quick start

```bash
cd "$(pwd)/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API endpoints

- `GET /` — health check
- `POST /auth/register` — register user
- `POST /auth/token` — login and get access token
- `GET /customers/` — list customers
- `POST /customers/` — create a new customer
- `GET /invoices/` — list invoices
- `POST /invoices/` — create an invoice
- `GET /workflows/` — list workflows
- `POST /workflows/` — create a workflow

## Next steps

1. add authentication dependency and token validation
2. implement frontend client UI
3. add subscription billing integration
4. deploy backend to a cloud service
