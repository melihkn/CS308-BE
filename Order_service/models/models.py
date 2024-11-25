from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Text, Boolean,
    ForeignKey, DateTime, DECIMAL, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, TEXT
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

# Customers Table
class Customer(Base):
    __tablename__ = 'customers'
    user_id = Column(CHAR(36), primary_key=True, nullable=False)
    name = Column(VARCHAR(50), nullable=False)
    middlename = Column(VARCHAR(50))
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    phone_number = Column(VARCHAR(20))
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")
    wishlists = relationship("Wishlist", back_populates="customer", cascade="all, delete-orphan")
    shopping_cart = relationship("ShoppingCart", back_populates="customer", cascade="all, delete-orphan")

# Category Table
class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"))
    category_name = Column(VARCHAR(100), nullable=False)
    parent_category = relationship("Category", remote_side=[category_id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent_category", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(CHAR(36), primary_key=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(VARCHAR(100), nullable=False)
    model = Column(VARCHAR(50), nullable=False)
    description = Column(TEXT)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"))
    serial_number = Column(VARCHAR(100), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer)
    distributor = Column(VARCHAR(100))
    image_url = Column(VARCHAR(255))
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    item_sold = Column(Integer, nullable=False, default=0)
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")


# Address Table
class Address(Base):
    __tablename__ = 'addresses'
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))
    street = Column(VARCHAR(255), nullable=False)
    city = Column(VARCHAR(100), nullable=False)
    state = Column(VARCHAR(100), nullable=False)
    zip_code = Column(VARCHAR(20), nullable=False)
    country = Column(VARCHAR(50), nullable=False)
    customer = relationship("Customer", back_populates="addresses")

# Orders Table
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="SET NULL"))
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_status = Column(VARCHAR(50), nullable=False)
    invoice_link = Column(VARCHAR(255)) # URL to the invoice -> can be null 
    order_status = Column(Integer, nullable=False)
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

# Order Items Table
class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    order_id = Column(CHAR(36), ForeignKey('orders.order_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False, default=1)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

# Wishlist Table
class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    customer = relationship("Customer", back_populates="wishlists")

# Shopping Cart Table
class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    customer = relationship("Customer", back_populates="shopping_cart")

# Review Table
class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)
    comment = Column(TEXT)
    customer = relationship("Customer", back_populates="reviews")


""" To be used later. 
# Refund Table
class Refund(Base):
    __tablename__ = 'refunds'
    refund_id = Column(CHAR(36), primary_key=True, nullable=False)
    order_id = Column(CHAR(36), ForeignKey('orders.order_id'))
    reason = Column(TEXT, nullable=False)
    status = Column(VARCHAR(50), nullable=False)
    order = relationship("Order", back_populates="refunds")
"""

# Pydantic models
from pydantic import BaseModel, Field
from typing import List, Optional

# Order Models
class OrderItemCreateSchema(BaseModel):
    product_id: str
    quantity: int
    price_at_purchase: float


class OrderCreateSchema(BaseModel):
    customer_id: str
    total_price: float
    order_date: str
    payment_status: str
    invoice_link: Optional[str]
    order_status: int
    items: List[OrderItemCreateSchema]

class OrderItemResponseSchema(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderResponseSchema(BaseModel):
    order_id: str
    customer_id: str
    total_price: float
    order_date: str
    payment_status: str
    invoice_link: Optional[str]
    order_status: int
    items: List[OrderItemResponseSchema]


class OrderStatusUpdateSchema(BaseModel):
    status: int


