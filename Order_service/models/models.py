# models.py
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List
from datetime import datetime
from utils.db_utils import Base

# SQLAlchemy Models
class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey("customers.user_id"), nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    order_status = Column(String(50), nullable=False)
    payment_status = Column(String(50), nullable=False)
    invoice_link = Column(String(255), nullable=True)

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(String(36), primary_key=True)
    product_id = Column(String(36), ForeignKey("products.product_id"), nullable=False)
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")

# this model for the format handling of order item creation the backend where requests are coming from the client side on the frontent
class OrderItemSchema(BaseModel):
    product_id: str
    quantity: int
    price_at_purchase: DECIMAL

# this model for the format handling of order creation
class OrderCreateSchema(BaseModel):
    customer_id: str
    items: List[OrderItemSchema]
    total_price: DECIMAL

# this model for the format handling of order response which is sent to the client when client wants the see the all orders 
class OrderResponseSchema(BaseModel):
    order_id: str
    customer_id: str
    total_price: DECIMAL
    order_date: datetime
    order_status: str
    payment_status: str
    items: List[OrderItemSchema]

# this model for the format handling of order status update
class OrderStatusUpdateSchema(BaseModel):
    status: str
