from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Agent])
def list_agents(owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.get_agents(db, owner_id)


@router.post("/", response_model=schemas.Agent)
def create_agent(agent: schemas.AgentCreate, owner_id: int = 1, db: Session = Depends(get_db)):
    return crud.create_agent(db, agent, owner_id)


@router.post("/{agent_id}/start", response_model=schemas.Agent)
def start_agent(agent_id: int, owner_id: int = 1, db: Session = Depends(get_db)):
    agent = crud.get_agent(db, agent_id, owner_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return crud.set_agent_status(db, agent, "running")


@router.post("/{agent_id}/stop", response_model=schemas.Agent)
def stop_agent(agent_id: int, owner_id: int = 1, db: Session = Depends(get_db)):
    agent = crud.get_agent(db, agent_id, owner_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return crud.set_agent_status(db, agent, "stopped")
