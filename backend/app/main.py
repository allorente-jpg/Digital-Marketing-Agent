from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine
from .routers import auth, customers, invoices, workflows

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Business Online Automation Hub",
    description="A starter backend for SMB workflow automation and recurring revenue management.",
    version="0.1.0",
)

app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(customers, prefix="/customers", tags=["customers"])
app.include_router(invoices, prefix="/invoices", tags=["invoices"])
app.include_router(workflows, prefix="/workflows", tags=["workflows"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", summary="Health check")
def root():
    return {"status": "ok", "project": "Business Online Automation Hub"}


@app.get("/health", summary="Application health")
def health():
    return {"status": "healthy"}
