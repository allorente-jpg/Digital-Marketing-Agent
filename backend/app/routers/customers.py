from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Customer)
def add_customer(customer: schemas.CustomerCreate, owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer, owner_id)


@router.get("/", response_model=List[schemas.Customer])
def list_customers(owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.get_customers(db, owner_id)
