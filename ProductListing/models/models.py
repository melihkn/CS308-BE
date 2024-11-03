from sqlalchemy import Column, String, Text, Integer, ForeignKey, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
import uuid

Base = declarative_base()

# SQLAlchemy Model
class ProductDB(Base):
    __tablename__ = 'products'

    # Columns
    product_id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    pm_id = Column(CHAR(36), ForeignKey('product_managers.pm_id', ondelete="SET NULL"), nullable=True)
    sm_id = Column(CHAR(36), ForeignKey('sales_managers.sm_id', ondelete="SET NULL"), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer, nullable=True)
    distributor = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"

# Pydantic Model for reading and responding
class Product(BaseModel):
    product_id: uuid.UUID
    name: str
    model: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    pm_id: Optional[str] = None
    sm_id: Optional[str] = None
    serial_number: str
    quantity: int
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None

     # Update to Pydantic v2 config
    class Config:
        from_attributes = True

# Pydantic Model for creating a product
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    model: str = Field(..., description="Product model")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = None
    pm_id: Optional[str] = None
    sm_id: Optional[str] = None
    serial_number: str
    quantity: int = Field(..., ge=0, description="Available quantity")
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None

# Pydantic Model for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    pm_id: Optional[str] = None
    sm_id: Optional[str] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None


