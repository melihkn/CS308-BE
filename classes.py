from sqlalchemy import Column, String, CHAR, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
