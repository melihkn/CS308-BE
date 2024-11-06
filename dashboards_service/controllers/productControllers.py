from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.productServices import get_products, create_product_service, update_product_service, delete_product_service
from dbContext import get_db
from models.models import Product
from pydantic import BaseModel, ConfigDict , Field
from typing import List
from datetime import datetime
from typing import Optional
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str
    model: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    pm_id: Optional[str] = None
    sm_id: Optional[str] = None
    serial_number: str
    quantity: int = 0
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

# ProductRead model for reading or returning product data
class ProductRead(ProductCreate):
    product_id: str


router = APIRouter()

@router.get("/products", response_model=List[ProductRead])
def read_discounts(db: Session = Depends(get_db)):
    return get_products(db)

