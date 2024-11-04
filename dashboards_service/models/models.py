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

# Admins Table
class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed password
    phone_number = Column(String(20))

# Product Managers Table
class ProductManager(Base):
    __tablename__ = 'product_managers'
    pm_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed password
    phone_number = Column(String(20))

# Sales Managers Table
class SalesManager(Base):
    __tablename__ = 'sales_managers'
    sm_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed password
    phone_number = Column(String(20))

# Category Table
class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id'))
    category_name = Column(String(100), nullable=False)

# Products Table
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    pm_id = Column(CHAR(36), ForeignKey('product_managers.pm_id'))
    sm_id = Column(CHAR(36), ForeignKey('sales_managers.sm_id'))
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer)
    distributor = Column(String(100))

# Orders Table
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    order_status = Column(String(50), nullable=False)
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

# Address Table
class Address(Base):
    __tablename__ = 'adres'
    customer_adres_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    address = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    name = Column(String(100))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))

# Wishlist Table
class Wishlist(Base):
    __tablename__ = 'wishlist'
    wishlist_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))
    wishlist_status = Column(String(50), nullable=False)

# Wishlist Items Table
class WishlistItem(Base):
    __tablename__ = 'wishlist_items'
    wishlist_item_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    wishlist_id = Column(CHAR(36), ForeignKey('wishlist.wishlist_id'))
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))

# Refund Table
class Refund(Base):
    __tablename__ = 'refund'
    refund_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    order_id = Column(CHAR(36), ForeignKey('orders.order_id'))
    order_item_id = Column(CHAR(36), ForeignKey('order_items.order_item_id'))
    request_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(50), nullable=False)
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    sm_id = Column(CHAR(36), ForeignKey('sales_managers.sm_id'))

# Delivery Table
class Delivery(Base):
    __tablename__ = 'delivery'
    delivery_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    order_id = Column(CHAR(36), ForeignKey('orders.order_id'))
    delivery_status = Column(String(50), nullable=False)
    addres_id = Column(CHAR(36), ForeignKey('adres.customer_adres_id'))

# Discount Table
class Discount(Base):
    __tablename__ = 'discount'
    discount_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))
    discount_rate = Column(DECIMAL(5, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

# Review Table
class Review(Base):
    __tablename__ = 'review'
    review_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    pm_id = Column(CHAR(36), ForeignKey('product_managers.pm_id'))
    approval_status = Column(String(50), nullable=False)

# Shopping Cart Table
class ShoppingCart(Base):
    __tablename__ = 'shoppingcart'
    cart_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id'))
    cart_status = Column(String(50), nullable=False)

# Shopping Cart Item Table
class ShoppingCartItem(Base):
    __tablename__ = 'shoppingcart_item'
    shopping_cart_item_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    cart_id = Column(CHAR(36), ForeignKey('shoppingcart.cart_id'))
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False, default=1)