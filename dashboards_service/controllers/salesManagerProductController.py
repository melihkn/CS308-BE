from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.productServices import get_products, create_product_service, update_product_service, delete_product_service, set_product_price
from dbContext import get_db
from models.models import Product
from pydantic import BaseModel, ConfigDict , Field
from typing import List
from datetime import datetime
from typing import Optional
from decimal import Decimal
from dependencies import verify_sm_role, oauth2_scheme

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
    price: Decimal = Field(default=0.00)
    cost: Decimal = Field(default=0.00)

    model_config = ConfigDict(arbitrary_types_allowed=True)

# ProductRead model for reading or returning product data
class ProductRead(ProductCreate):
    product_id: str

class SetPriceRequest(BaseModel):
    price: Decimal

router = APIRouter()

@router.get("/products", response_model=List[ProductRead],dependencies=[Depends(verify_sm_role)])
def read_discounts(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_products(db)

@router.patch("/products/{product_id}/set-price", response_model=ProductRead,dependencies=[Depends(verify_sm_role)])
def set_product_price_endpoint(product_id: str, price_data: SetPriceRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    product = set_product_price(db, product_id, price_data.price)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product