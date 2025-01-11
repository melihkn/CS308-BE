from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.discountServices import get_discounts, create_discount_service, update_discount_service, delete_discount_service
from dbContext import get_db
from models.models import Discount
from pydantic import BaseModel, ConfigDict , Field
from typing import List
from datetime import datetime
from dependencies import verify_sm_role, oauth2_scheme
router = APIRouter()

class DiscountCreate(BaseModel):
    product_id: str
    discount_rate: float
    start_date: datetime
    end_date: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

@router.get("/discounts", response_model=List[DiscountCreate],dependencies=[Depends(verify_sm_role)])
def read_discounts(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_discounts(db)

@router.post("/discounts", response_model=DiscountCreate,dependencies=[Depends(verify_sm_role)])
def create_discount(discount: DiscountCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return create_discount_service(db, discount)
