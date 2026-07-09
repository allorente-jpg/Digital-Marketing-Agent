from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine
from .routers import auth, customers, invoices, workflows

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digital Marketing Agent",
    description="Backend for a digital marketing agency: clients, invoices, and marketing workflow automation.",
    version="0.1.0",
)

# Dev CORS: allow the Vite dev server (and any local origin) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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
    return {"status": "ok", "project": "Digital Marketing Agent"}


@app.get("/health", summary="Application health")
def health():
    return {"status": "healthy"}
