from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_customer(db: Session, customer: schemas.CustomerCreate, owner_id: int):
    db_customer = models.Customer(**customer.dict(), owner_id=owner_id)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customers(db: Session, owner_id: int):
    return db.query(models.Customer).filter(models.Customer.owner_id == owner_id).all()


def create_invoice(db: Session, invoice: schemas.InvoiceCreate, owner_id: int):
    db_invoice = models.Invoice(**invoice.dict(), owner_id=owner_id, status="draft")
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def get_invoices(db: Session, owner_id: int):
    return db.query(models.Invoice).filter(models.Invoice.owner_id == owner_id).all()


def create_workflow(db: Session, workflow: schemas.WorkflowCreate, owner_id: int):
    db_workflow = models.Workflow(**workflow.dict(), owner_id=owner_id)
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow


def get_workflows(db: Session, owner_id: int):
    return db.query(models.Workflow).filter(models.Workflow.owner_id == owner_id).all()
