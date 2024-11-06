# app/models/product_manager.py
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from ..dbContext import Base
import uuid

class ProductManager(Base):
    __tablename__ = 'product_managers'

    pm_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    middlename = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)


