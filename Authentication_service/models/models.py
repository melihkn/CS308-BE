from sqlalchemy import Column, String, Integer
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
