import uuid
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Integer, VARCHAR, CHAR, Text, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List
from datetime import datetime
from Order_service.utils.db_utils import Base

# SQLAlchemy Models

class Customer(Base):
    __tablename__ = "customers"

    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    name = Column(VARCHAR(50), nullable=False, extend_existing=True)
    middlename = Column(VARCHAR(50), nullable=True, extend_existing=True)
    surname = Column(VARCHAR(50), nullable=False, extend_existing=True)
    email = Column(VARCHAR(100), unique=True, nullable=False, extend_existing=True)
    password = Column(VARCHAR(255), nullable=False, extend_existing=True)
    phone_number = Column(VARCHAR(20), nullable=True, extend_existing=True)

    orders = relationship("Order", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")
    wishlists = relationship("Wishlist", back_populates="customer")

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True, extend_existing=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id'), nullable=True, extend_existing=True)
    category_name = Column(VARCHAR(100), nullable=False, extend_existing=True)

    subcategories = relationship("Category", backref='parent', remote_side=[category_id])
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    name = Column(VARCHAR(100), nullable=False, extend_existing=True)
    model = Column(VARCHAR(50), nullable=False, extend_existing=True)
    description = Column(Text, nullable=True, extend_existing=True)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete='SET NULL'), nullable=True, extend_existing=True)
    serial_number = Column(VARCHAR(100), unique=True, nullable=False, extend_existing=True)
    quantity = Column(Integer, nullable=False, default=0, extend_existing=True)
    warranty_status = Column(Integer, nullable=True, extend_existing=True)
    distributor = Column(VARCHAR(100), nullable=True, extend_existing=True)
    image_url = Column(VARCHAR(255), nullable=True, extend_existing=True)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00, extend_existing=True)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    customer_id = Column(CHAR(36), ForeignKey("customers.user_id"), extend_existing=True)
    total_price = Column(DECIMAL(10, 2), nullable=False, extend_existing=True)
    order_date = Column(DateTime, default=datetime.utcnow, extend_existing=True)
    order_status = Column(VARCHAR(50), nullable=False, extend_existing=True)
    payment_status = Column(VARCHAR(50), nullable=False, extend_existing=True)
    invoice_link = Column(VARCHAR(255), nullable=True, extend_existing=True)
    items = relationship("OrderItem", back_populates="order")

    customer = relationship("Customer", back_populates="orders")
    refunds = relationship("Refund", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    product_id = Column(CHAR(36), ForeignKey("products.product_id"), extend_existing=True)
    order_id = Column(CHAR(36), ForeignKey("orders.order_id"), extend_existing=True)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False, extend_existing=True)
    quantity = Column(Integer, nullable=False, default=1, extend_existing=True)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    name = Column(VARCHAR(50), nullable=False, extend_existing=True)
    middlename = Column(VARCHAR(50), nullable=True, extend_existing=True)
    surname = Column(VARCHAR(50), nullable=False, extend_existing=True)
    email = Column(VARCHAR(100), unique=True, nullable=False, extend_existing=True)
    password = Column(VARCHAR(255), nullable=False, extend_existing=True)
    phone_number = Column(VARCHAR(20), nullable=True, extend_existing=True)

class ProductManager(Base):
    __tablename__ = "product_managers"

    pm_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    name = Column(VARCHAR(50), nullable=False, extend_existing=True)
    middlename = Column(VARCHAR(50), nullable=True, extend_existing=True)
    surname = Column(VARCHAR(50), nullable=False, extend_existing=True)
    email = Column(VARCHAR(100), unique=True, nullable=False, extend_existing=True)
    password = Column(VARCHAR(255), nullable=False, extend_existing=True)
    phone_number = Column(VARCHAR(20), nullable=True, extend_existing=True)

class SalesManager(Base):
    __tablename__ = "sales_managers"

    sm_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    name = Column(VARCHAR(50), nullable=False, extend_existing=True)
    middlename = Column(VARCHAR(50), nullable=True, extend_existing=True)
    surname = Column(VARCHAR(50), nullable=False, extend_existing=True)
    email = Column(VARCHAR(100), unique=True, nullable=False, extend_existing=True)
    password = Column(VARCHAR(255), nullable=False, extend_existing=True)
    phone_number = Column(VARCHAR(20), nullable=True, extend_existing=True)

class Address(Base):
    __tablename__ = "adres"

    customer_adres_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    address = Column(Text, nullable=False, extend_existing=True)
    type = Column(VARCHAR(50), nullable=False, extend_existing=True)
    name = Column(VARCHAR(100), nullable=True, extend_existing=True)
    customer_id = Column(CHAR(36), ForeignKey("customers.user_id"), extend_existing=True)

    customer = relationship("Customer", back_populates="addresses")

class Wishlist(Base):
    __tablename__ = "wishlist"

    wishlist_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    customer_id = Column(CHAR(36), ForeignKey("customers.user_id"), extend_existing=True)
    wishlist_status = Column(VARCHAR(50), nullable=False, extend_existing=True)

    customer = relationship("Customer", back_populates="wishlists")
    items = relationship("WishlistItem", back_populates="wishlist")

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    wishlist_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    wishlist_id = Column(CHAR(36), ForeignKey("wishlist.wishlist_id"), extend_existing=True)
    product_id = Column(CHAR(36), ForeignKey("products.product_id"), extend_existing=True)

    wishlist = relationship("Wishlist", back_populates="items")
    product = relationship("Product")

class Refund(Base):
    __tablename__ = "refund"

    refund_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    order_id = Column(CHAR(36), ForeignKey("orders.order_id"), extend_existing=True)
    order_item_id = Column(CHAR(36), ForeignKey("order_items.order_item_id"), extend_existing=True)
    request_date = Column(DateTime, default=datetime.utcnow, extend_existing=True)
    status = Column(VARCHAR(50), nullable=False, extend_existing=True)
    refund_amount = Column(DECIMAL(10, 2), nullable=False, extend_existing=True)

    order = relationship("Order")
    order_item = relationship("OrderItem")
    sales_manager = relationship("SalesManager", back_populates="refunds")

class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    order_id = Column(CHAR(36), ForeignKey("orders.order_id"), extend_existing=True)
    delivery_status = Column(VARCHAR(50), nullable=False, extend_existing=True)
    addres_id = Column(CHAR(36), ForeignKey("adres.customer_adres_id"), extend_existing=True)

    order = relationship("Order")
    address = relationship("Address")

class Discount(Base):
    __tablename__ = "discount"

    discount_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    product_id = Column(CHAR(36), ForeignKey("products.product_id"), extend_existing=True)
    discount_rate = Column(DECIMAL(5, 2), nullable=False, extend_existing=True)
    start_date = Column(DateTime, nullable=False, extend_existing=True)
    end_date = Column(DateTime, nullable=False, extend_existing=True)
    is_active = Column(Boolean, nullable=False, default=True, extend_existing=True)

    product = relationship("Product")

class Review(Base):
    __tablename__ = "review"

    review_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    customer_id = Column(CHAR(36), ForeignKey("customers.user_id"), extend_existing=True)
    product_id = Column(CHAR(36), ForeignKey("products.product_id"), extend_existing=True)
    rating = Column(Integer, nullable=False, extend_existing=True)
    comment = Column(Text, nullable=True, extend_existing=True)
    approval_status = Column(VARCHAR(50), nullable=False, extend_existing=True)

    customer = relationship("Customer")
    product = relationship("Product")

class ShoppingCart(Base):
    __tablename__ = "shoppingcart"

    cart_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    customer_id = Column(CHAR(36), ForeignKey("customers.user_id"), extend_existing=True)
    cart_status = Column(VARCHAR(50), nullable=False, extend_existing=True)

    customer = relationship("Customer")
    items = relationship("ShoppingCartItem", back_populates="cart")

class ShoppingCartItem(Base):
    __tablename__ = "shoppingcart_item"

    shopping_cart_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), extend_existing=True)
    cart_id = Column(CHAR(36), ForeignKey("shoppingcart.cart_id"), extend_existing=True)
    product_id = Column(CHAR(36), ForeignKey("products.product_id"), extend_existing=True)
    quantity = Column(Integer, nullable=False, default=1, extend_existing=True)

    cart = relationship("ShoppingCart", back_populates="items")
    product = relationship("Product")

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
