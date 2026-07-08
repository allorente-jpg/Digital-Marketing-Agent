from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.create_invoice(db, invoice, owner_id)


@router.get("/", response_model=List[schemas.Invoice])
def list_invoices(owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.get_invoices(db, owner_id)
