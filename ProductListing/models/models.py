from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

Base = declarative_base()

# SQLAlchemy Model for Products
class ProductDB(Base):
    __tablename__ = "products"

    # Columns
    product_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Matches CHAR(36)
    name = Column(String(100), nullable=False)  # Product name
    model = Column(String(50), nullable=False)  # Product model
    description = Column(Text, nullable=True)  # Product description
    category_id = Column(Integer, ForeignKey("category.category_id", ondelete="SET NULL"), nullable=True)  # Category FK
    item_sold = Column(Integer, nullable=True, default=0)  # Items sold
    price = Column(Float, nullable=True)  # Product price
    cost = Column(Float, nullable=True)  # Product cost
    serial_number = Column(String(100), unique=True, nullable=False)  # Serial number
    quantity = Column(Integer, nullable=False, default=0)  # Quantity in stock
    warranty_status = Column(Integer, nullable=True)  # Warranty in months
    distributor = Column(String(100), nullable=True)  # Distributor
    
    # Relationships
    reviews = relationship("ReviewDB", back_populates="product")  # Relationship with reviews

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"


# SQLAlchemy Model for Reviews
class ReviewDB(Base):
    __tablename__ = "reviews"

    # Columns
    review_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String(36), nullable=False)  # FK for customers (assumed)
    product_id = Column(String(36), ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)  # FK for products
    rating = Column(Integer, nullable=False)  # Product rating
    comment = Column(Text, nullable=True)  # Optional comment
    approval_status = Column(String(50), nullable=False)  # Approval status

    # Relationship back to product
    product = relationship("ProductDB", back_populates="reviews")

    def __repr__(self):
        return f"<Review(rating={self.rating}, comment={self.comment[:20]})>"


# SQLAlchemy Model for Category
class Category(Base):
    __tablename__ = "category"

    # Columns
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey("category.category_id"), nullable=True)  # FK to itself for hierarchy
    category_name = Column(String(100), nullable=False)  # Name of the category

    def __repr__(self):
        return f"<Category(category_name={self.category_name}, parentcategory_id={self.parentcategory_id})>"


# SQLAlchemy Model for Product Popularity (if needed)
class ProductPopularity(Base):
    __tablename__ = "product_popularity"

    # Columns
    product_id = Column(String(36), ForeignKey("products.product_id", ondelete="CASCADE"), primary_key=True)  # FK to products
    popularity_score = Column(Float, index=True)  # Popularity score
    last_updated = Column(DateTime, default=datetime.utcnow)  # Timestamp of last update

    # Relationship
    product = relationship("ProductDB")

    def __repr__(self):
        return f"<ProductPopularity(product_id={self.product_id}, score={self.popularity_score})>"


# Pydantic Models for Validation and Data Serialization


# Pydantic Model for Products
class Product(BaseModel):
    product_id: uuid.UUID
    name: str
    model: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    item_sold: Optional[int] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    serial_number: str
    quantity: int
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None

    class Config:
        orm_mode = True  # Allows ORM objects to be serialized


# Pydantic Model for Creating a Product
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    model: str = Field(..., description="Product model")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = None
    item_sold: Optional[int] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    serial_number: str
    quantity: int = Field(..., ge=0, description="Available quantity")
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None


# Pydantic Model for Updating a Product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    item_sold: Optional[int] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None
