from sqlalchemy import (
    Column, String, Integer, ForeignKey, Text,
    DECIMAL, DateTime, CHAR, VARCHAR
)
from sqlalchemy.orm import relationship, declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

# Customers Table
class Customer(Base):
    __tablename__ = 'customers'

    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(VARCHAR(50), nullable=False)
    middlename = Column(VARCHAR(50), nullable=True)
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    phone_number = Column(VARCHAR(20), nullable=True)

    # Relationships
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")
    wishlists = relationship("Wishlist", back_populates="customer", cascade="all, delete-orphan")
    shopping_cart = relationship("ShoppingCart", back_populates="customer", cascade="all, delete-orphan")


# Address Table
class Address(Base):
    __tablename__ = 'adres'

    customer_adres_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    address = Column(Text, nullable=False)
    type = Column(VARCHAR(50), nullable=False)
    name = Column(VARCHAR(100), nullable=True)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="addresses")


# Orders Table
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="SET NULL"), nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_status = Column(VARCHAR(50), nullable=False)
    invoice_link = Column(VARCHAR(255), nullable=True)
    order_status = Column(Integer, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


# Order Items Table
class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"), nullable=True)
    order_id = Column(CHAR(36), ForeignKey('orders.order_id', ondelete="CASCADE"), nullable=True)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    order = relationship("Order", back_populates="order_items") # order items has order relationship 
    product = relationship("Product", back_populates="order_items") # order items has product relationship 


# Products Table
class Product(Base):
    __tablename__ = 'products'

    product_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(VARCHAR(100), nullable=False)
    model = Column(VARCHAR(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    serial_number = Column(VARCHAR(100), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer, nullable=True)
    distributor = Column(VARCHAR(100), nullable=True)
    image_url = Column(VARCHAR(255), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    item_sold = Column(Integer, nullable=False, default=0)

    # Relationships -> a product can have multiple reviews, order items, wishlist items, and shopping cart items

    # back_populates is used to define the relationship from the other side which means the other side of the relationship should have the same name
    category = relationship("Category", back_populates="products") # product has category relationship 
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan") # product has order items relationship 
    wishlist_items = relationship("WishlistItem", back_populates="product", cascade="all, delete-orphan") # product has wishlist items relationship 
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan") # product has reviews relationship 
    shopping_cart_items = relationship("ShoppingCartItem", back_populates="product", cascade="all, delete-orphan") # product has shopping cart items relationship


# Category Table
class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    category_name = Column(VARCHAR(100), nullable=False)

    # Relationships
    subcategories = relationship("Category", back_populates="parent_category", cascade="all, delete-orphan")
    parent_category = relationship("Category", remote_side=[category_id], back_populates="subcategories")
    products = relationship("Product", back_populates="category")


# Wishlist Table
class Wishlist(Base):
    __tablename__ = 'wishlist'

    wishlist_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"), nullable=True)
    wishlist_status = Column(VARCHAR(50), nullable=False)
    name = Column(VARCHAR(255), nullable=False, default="Unnamed Wishlist")

    # Relationships
    customer = relationship("Customer", back_populates="wishlists")
    wishlist_items = relationship("WishlistItem", back_populates="wishlist", cascade="all, delete")


# Wishlist Items Table
class WishlistItem(Base):
    __tablename__ = 'wishlist_items'

    wishlist_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    wishlist_id = Column(CHAR(36), ForeignKey('wishlist.wishlist_id', ondelete="CASCADE"), nullable=True) # wishlist silinirse wishlist itemlar da silinir 
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"), nullable=True) # product silinirse wishlist itemlar da silinir 

    # Relationships
    wishlist = relationship("Wishlist", back_populates="wishlist_items") # wishlist item has wishlist relationship 
    product = relationship("Product", back_populates="wishlist_items") # wishlist item has product relationship 


# Shopping Cart Table
class ShoppingCart(Base):
    __tablename__ = 'shoppingcart'

    cart_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))
    cart_status = Column(VARCHAR(50), nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="shopping_cart")
    items = relationship("ShoppingCartItem", back_populates="cart", cascade="all, delete-orphan")


# Shopping Cart Items Table
class ShoppingCartItem(Base):
    __tablename__ = 'shoppingcart_item'

    shopping_cart_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    cart_id = Column(CHAR(36), ForeignKey('shoppingcart.cart_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    cart = relationship("ShoppingCart", back_populates="items")
    product = relationship("Product", back_populates="shopping_cart_items")


# Review Table
class Review(Base):
    __tablename__ = 'review'

    review_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    approval_status = Column(VARCHAR(50), nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
