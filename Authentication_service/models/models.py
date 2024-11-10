from sqlalchemy import Column, String, Integer, CHAR, VARCHAR
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    middlename = Column(String, nullable=True)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone_number = Column(String, nullable=True)

class ProductManager(Base):
    __tablename__ = "product_managers"

    pm_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(VARCHAR(50), nullable=False)
    middlename = Column(VARCHAR(50), nullable=True)
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    phone_number = Column(VARCHAR(20), nullable=True)

class SalesManager(Base):
    __tablename__ = "sales_managers"

    sm_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(VARCHAR(50), nullable=False)
    middlename = Column(VARCHAR(50), nullable=True)
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    phone_number = Column(VARCHAR(20), nullable=True)

class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(VARCHAR(50), nullable=False)
    middlename = Column(VARCHAR(50), nullable=True)
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    phone_number = Column(VARCHAR(20), nullable=True)
