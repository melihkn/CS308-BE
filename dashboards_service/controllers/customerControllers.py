from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from services.customerService import get_customers
from models.models import Customer
from dbContext import get_db
from typing import List, Optional



router = APIRouter()
"""
  {
    "name": "string",
    "middlename": "string",
    "surname": "string",
    "email": "string",
    "phone": "string",
    "customer_id": "string"
  }
"""
class CustomerCreate(BaseModel):
    user_id: str  
    name: str
    middlename: Optional[str] = None
    surname: str
    email: str
    phone_number: Optional[str] = None
    

    model_config = ConfigDict(arbitrary_types_allowed=True)


    


@router.get("/customers", response_model=List[CustomerCreate])
def read_customers(db: Session = Depends(get_db)):
    return get_customers(db)