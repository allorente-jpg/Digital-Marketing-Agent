# Business Online Desktop App

A desktop version of the Business Online app using Tkinter and the shared backend models.

## Requirements

- Python 3.11
- The backend virtual environment at `../backend/.venv`

## Install and run

```bash
cd "/Users/alejandrollorente/Documents/Claude/Projects/Business Online/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd "/Users/alejandrollorente/Documents/Claude/Projects/Business Online/desktop"
python3 main.py
```

## What it does

- Add and list customers
- Create and list invoices
- Create and list workflows
- Reuses the backend database and models

## Notes

The desktop app uses the database and data access layer from `../backend/app`. If you make changes to backend models or CRUD operations, the desktop app will use the same data schema.
