from sqlalchemy import (
    Column, String, Integer, CHAR, ForeignKey, DECIMAL, Text, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import CHAR
import uuid
from datetime import datetime

Base = declarative_base()

# Utility function for UUID
def generate_uuid():
    return str(uuid.uuid4())

# Customers Table
class Customer(Base):
    __tablename__ = 'customers'
    user_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed password
    phone_number = Column(String(20))


# Products Table
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    item_sold = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL(10, 2), nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer)
    distributor = Column(String(100))
    image_url = Column(String(255))

# Orders Table
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    order_status = Column(Integer, nullable=False)
    payment_status = Column(String(50), nullable=False)
    invoice_link = Column(String(255))

# Order Items Table
class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))
    order_id = Column(CHAR(36), ForeignKey('orders.order_id'))
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

# Review Table
class Review(Base):
    __tablename__ = 'review'
    review_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete='CASCADE'))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete='CASCADE'))
    rating = Column(Integer, nullable=False)  # Add custom validation for 1 to 5 rating
    comment = Column(Text)
    approval_status = Column(String(50), nullable=False)  # e.g., 'pending', 'approved', 'rejected'

    # Relationships
    customer = relationship('Customer', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')

# Add back_populates to Customer and Product classes
Customer.reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')
Product.reviews = relationship('Review', back_populates='product', cascade='all, delete-orphan')
