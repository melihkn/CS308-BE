from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List
from datetime import datetime
from utils.db_utils import Base

# SQLAlchemy Models

class Customer(Base):
    __tablename__ = "customers"

    user_id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = 'products'

    # columns of the table
    product_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(VARCHAR(100), nullable=False)
    model = Column(VARCHAR(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete='SET NULL'), nullable=True)
    serial_number = Column(VARCHAR(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer, nullable=True)
    distributor = Column(VARCHAR(100), nullable=True)
    image_url = Column(VARCHAR(255), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    item_sold = Column(Integer, nullable=False, default=0)

    # defining the relationship between the tables
    order_items = relationship("OrderItem", back_populates="product")
    

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"



class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(String(36), ForeignKey("customers.user_id"), nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    order_status = Column(String(50), nullable=False)  # String-based statuses
    payment_status = Column(String(50), nullable=False)
    invoice_link = Column(String(255), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")  # Define relationship to Customer
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    refunds = relationship("Refund", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    product_id = Column(String(36), ForeignKey("products.product_id"), nullable=False)
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Refund(Base):
    __tablename__ = "refunds"

    refund_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False)
    order_item_id = Column(String(36), ForeignKey("order_items.order_item_id"), nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), nullable=False)  # e.g., 'pending', 'approved', 'rejected'
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    sm_id = Column(String(36), ForeignKey("sales_managers.sm_id"), nullable=True)

    # Relationships
    order = relationship("Order", back_populates="refunds")  # Links to Order
    order_item = relationship("OrderItem", back_populates="refunds")  # Links to OrderItem
    sales_manager = relationship("SalesManager", back_populates="refunds")  # Links to SalesManager


# Pydantic Models

class OrderStatusUpdateSchema(BaseModel):
    status: int

class RefundResponseSchema(BaseModel):
    message: str
    refund_amount: float
    refunded_product: str
    updated_stock: int

class OrderItemSchema(BaseModel):
    product_id: str
    quantity: int
    price_at_purchase: float


class OrderCreateSchema(BaseModel):
    customer_id: str
    items: List[OrderItemSchema]
    total_price: float


class OrderResponseSchema(BaseModel):
    order_id: str
    customer_id: str
    total_price: float
    order_date: datetime
    order_status: str
    payment_status: str
    items: List[OrderItemSchema]

    class Config:
        orm_mode = True
