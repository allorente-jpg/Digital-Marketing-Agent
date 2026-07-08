from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class InvoiceBase(BaseModel):
    customer_id: int
    amount: float
    due_date: Optional[str] = None
    description: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    trigger: str
    action: str


class WorkflowCreate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
