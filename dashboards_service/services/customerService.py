from sqlalchemy.orm import Session 
from models.models import  Customer
from datetime import datetime

def get_customers(db: Session):
    return db.query(Customer).all()