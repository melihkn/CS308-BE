from sqlalchemy import Column, String, CHAR, Integer, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

# User types
class Customer(Base):
    __tablename__ = "customers"

    # This line is crucial for the database to work properly.
    # Eğer auto increment olmazsa: user_id user dan alınmadığından dolayı hata alırız. 
    user_id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String)
    middlename = Column(String, nullable=True)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone_number = Column(String, nullable=True)

class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(CHAR(36), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20))

class ProductManager(Base):
    __tablename__ = 'product_managers'
    pm_id = Column(CHAR(36), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20))

class SalesManager(Base):
    __tablename__ = 'sales_managers'
    sm_id = Column(CHAR(36), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    middlename = Column(String(50))
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20))


# uuid will help us to generate unique ids for the shopping cart and shopping cart  
class ShoppingCart(Base):
    __tablename__ = 'shoppingcart' # name of the table in the database
    cart_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # primary key
    customer_id = Column(String(36), ForeignKey('customers.user_id'), nullable=True) # foreign key
    cart_status = Column(String(50), nullable=False) # status of the cart (active, inactive, ordered)

    # when we define relationship in orm, we give name of the class, not the table name and the back_populates parameter is used to define the relationship in the other class
    items = relationship("ShoppingCartItem", back_populates="cart") # one-to-many relationship

class ShoppingCartItem(Base):
    __tablename__ = 'shoppingcart_item'
    shopping_cart_item_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_id = Column(String(36), ForeignKey('shoppingcart.cart_id'))
    product_id = Column(String(36), ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("ShoppingCart", back_populates="items") # many-to-one relationship



class Product(Base):
    __tablename__ = 'products'

    # Columns
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    item_sold = Column(Integer, nullable=True)
    price = Column(float, nullable=True)
    cost = Column(float, nullable=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer, nullable=True)
    distributor = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)  # for the relative path of the image in the backend

    def __repr__(self):
        return f"<Product(name={self.name}, model={self.model}, quantity={self.quantity})>"
