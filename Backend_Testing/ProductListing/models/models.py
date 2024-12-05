from sqlalchemy import Column, String, Text, Integer, ForeignKey, CHAR, Float, DateTime, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict


Base = declarative_base()

# SQLAlchemy Model
class ProductDB(Base):
    __tablename__ = 'products'

    product_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    item_sold = Column(Integer, nullable=False, default=0)  # Track total quantity sold
    warranty_status = Column(Integer, nullable=True)
    distributor = Column(String(100), nullable=True) 
    image_url = Column(String(255), nullable=True)
    price = Column(DECIMAL(10,2), nullable=False)  
    cost = Column(DECIMAL(10,2), nullable=False)   
    # Relationship to reviews
    reviews = relationship("Review", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"

class Review(Base):
    __tablename__ = 'review'
    review_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    pm_id = Column(CHAR(36), ForeignKey('product_managers.pm_id'))
    approval_status = Column(String(50), nullable=False)
    
    # Relationship to product
    product = relationship("ProductDB", back_populates="reviews")

class Customer(Base):
    __tablename__ = 'customers'
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed password
    phone_number = Column(String(20))


# Model for ProductPopularity
class ProductPopularity(Base):
    __tablename__ = 'product_popularity'

    product_id = Column(String(36), ForeignKey('products.product_id'), primary_key=True)
    popularity_score = Column(Float, index=True)  # Precomputed popularity score
    last_updated = Column(DateTime, default=datetime.utcnow)

# Pydantic Model for Product
class Product(BaseModel):
    product_id: str
    name: str
    model: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    quantity: int
    price: float 
    cost: float 
    item_sold: int 
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None
    
     
    

    model_config = ConfigDict(from_attributes=True)



class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id'), nullable=True)
    category_name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Category(category_name={self.category_name}, parentcategory_id={self.parentcategory_id})>"
    
# Product Managers Table
class ProductManager(Base):
    __tablename__ = 'product_managers'
    pm_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed password
    phone_number = Column(String(20))

# Pydantic Model for creating a product
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    model: str = Field(..., description="Product model")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = None
    serial_number: str
    quantity: int = Field(..., ge=0, description="Available quantity")
    price: float = Field(..., description="Selling price of the product")
    cost: float = Field(..., description="Cost price of the product")
    item_sold: int = Field(0, description="Total items sold")  # Default 0
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None
    
    

# Pydantic Model for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str]
    model: Optional[str]
    description: Optional[str]
    category_id: Optional[int]
    serial_number: Optional[str]
    quantity: Optional[int]
    price: Optional[float]
    cost: Optional[float]
    item_sold: Optional[int]
    warranty_status: Optional[str]
    distributor: Optional[str]
    image_url: Optional[str]
