from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.customerService import get_customers
from models.models import Customer
from dbContext import get_db
from typing import List



router = APIRouter()


@router.get("/customers", response_model=List[Customer])
def read_customers(db: Session = Depends(get_db)):
    return get_customers(db)