from sqlalchemy import (
    Column, String, Integer, Text,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.mysql import CHAR, VARCHAR

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

class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="wishlists")
    items = relationship("WishlistItem", back_populates="wishlist")

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)  # Reference to the product in your product database
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"))
    wishlist = relationship("Wishlist", back_populates="items")
    notes = Column(Text, nullable=True)  # Optional field for item notes

    
    
