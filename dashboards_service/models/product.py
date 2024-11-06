# app/models/product.py
import uuid
from sqlalchemy import Column, String, Integer, Text, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from ..dbContext import Base

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    warranty_status = Column(Integer, nullable=True)  # Months
    distributor = Column(String(100), nullable=True)

    category = relationship("Category", back_populates="products")
    product_manager = relationship("ProductManager", back_populates="products")
    sales_manager = relationship("SalesManager", back_populates="products")
    reviews = relationship("Review", back_populates="product")
