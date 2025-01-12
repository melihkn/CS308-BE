from sqlalchemy import Column, String, Text, Integer, ForeignKey, CHAR, Float, DateTime, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
Base = declarative_base()

# SQLAlchemy Model
class ProductDB(Base):
    __tablename__ = 'products'

    product_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL, nullable=False)   # Track total quantity sold
    distributor = Column(String(100), nullable=True) 
    image_url = Column(String(255), nullable=True)
    item_sold = Column(Integer, nullable=False, default=0) 
    warranty_status = Column(Integer, nullable=True)
    cost = Column(DECIMAL, nullable=False)   
    # Relationship to reviews
    discounts = relationship("Discount", back_populates="product")
    reviews = relationship("ReviewDB", back_populates="product")
    

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"
    
class Discount(Base):
    __tablename__ = "discount"

    discount_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.product_id", ondelete="CASCADE"), nullable=True)
    discount_rate = Column(DECIMAL(5, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Integer, nullable=False, default=1)

    product = relationship("ProductDB", back_populates="discounts")

class ProductSchema(BaseModel):
    product_id: str
    name: str
    model: str
    description: Optional[str]
    serial_number: str
    category_id: Optional[int]
    quantity: int
    price: float
    distributor: Optional[str]
    image_url: Optional[str]
    item_sold: int
    warranty_status: Optional[int]
    cost: float
    
    class Config:
        from_attributes = True

class ProductDiscountSchema(BaseModel):
    product_id: str
    name: str
    model: str
    description: Optional[str] = None
    serial_number: Optional[str] = None
    category_id: Optional[int] = None
    quantity: int
    price: float
    distributor: Optional[str] = None
    image_url: Optional[str] = None
    item_sold: Optional[int] = 0
    warranty_status: Optional[int] = None
    cost: Optional[float] = 0.0

    discount_rate: Optional[float] = 0.0
    end_date: Optional[datetime] = None

    average_rating: Optional[float] = None

    class Config:
        from_attributes = True


# SQLAlchemy Model for Reviews
class ReviewDB(Base):
    __tablename__ = 'review'

    review_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String(36), nullable=False)
    product_id = Column(String(36), ForeignKey('products.product_id', ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    approval_status = Column(String(50), nullable=False)

    # Relationship back to product
    product = relationship("ProductDB", back_populates="reviews")

# Model for ProductPopularity
class ProductPopularity(Base):
    __tablename__ = 'product_popularity'

    product_id = Column(String(36), ForeignKey('products.product_id'), primary_key=True)
    popularity_score = Column(Float, index=True)  # Precomputed popularity score
    last_updated = Column(DateTime, default=datetime.utcnow)

# Pydantic Model for Product
class Product(BaseModel):
    product_id: uuid.UUID
    name: str
    model: str
    description: Optional[str] = None
    quantity: int
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None
    item_sold: int  
    price: float 
    cost: float  
    category_id: Optional[int] = None
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True



class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id'), nullable=True)
    category_name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Category(category_name={self.category_name}, parentcategory_id={self.parentcategory_id})>"


class CategoryDB(Base):
    __tablename__ = "category"  # Table name in the database

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey("category.category_id", ondelete="SET NULL"), nullable=True)
    category_name = Column(String(100), nullable=False)

    # Add extend_existing=True to avoid redefinition errors
    __table_args__ = {"extend_existing": True}

    # Relationship to reference parent and children categories
    parent = relationship("CategoryDB", remote_side=[category_id], backref="children")

    def __repr__(self):
        return f"<CategoryDB(category_id={self.category_id}, category_name={self.category_name}, parentcategory_id={self.parentcategory_id})>"
    

# Pydantic Model for creating a product
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    model: str = Field(..., description="Product model")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = None
    serial_number: str
    quantity: int = Field(..., ge=0, description="Available quantity")
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None
    item_sold: int = Field(0, description="Total items sold")  # Default 0
    price: float = Field(..., description="Selling price of the product")
    cost: float = Field(..., description="Cost price of the product")

# Pydantic Model for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None
    item_sold: Optional[int] = None  # Allow updates
    price: Optional[float] = None  # Allow updates
    cost: Optional[float] = None  # Allow updates


class user2(BaseModel):
    username: Optional[str] = None
