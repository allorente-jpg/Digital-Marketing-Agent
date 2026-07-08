from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Workflow)
def create_workflow(workflow: schemas.WorkflowCreate, owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.create_workflow(db, workflow, owner_id)


@router.get("/", response_model=List[schemas.Workflow])
def list_workflows(owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.get_workflows(db, owner_id)
