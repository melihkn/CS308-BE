from decimal import Decimal
from sqlalchemy.orm import Session
from models.models import Product
from datetime import datetime


def get_products(db: Session):
    return db.query(Product).all()

def create_product_service(db: Session, product_data):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product_service(db: Session, product_id: str, product_data):
    product = db.query(Product).filter_by(product_id=product_id).first()
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product_service(db: Session, product_id: str):
    product = db.query(Product).filter_by(product_id=product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return {"message": "product deleted successfully"}

def set_product_price(db: Session, product_id: str, new_price: Decimal):
    product = db.query(Product).filter_by(product_id=product_id).first()
    if not product:
        return None
    product.price = new_price
    db.commit()
    db.refresh(product)
    return product
