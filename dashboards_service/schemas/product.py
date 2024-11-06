from pydantic import BaseModel, Field, validator
from typing import Optional
import uuid

class ProductBase(BaseModel):
    name: str
    model: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    serial_number: str
    quantity: int = 0
    warranty_status: Optional[int] = None  # Months
    distributor: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None

class ProductOut(ProductBase):
    product_id: str

    class Config:
        orm_mode = True
