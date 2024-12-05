from typing import Optional
from sqlalchemy.orm import Session
from models.models import Product
from datetime import datetime
#from controllers.productControllers import ProductCreate, ProductUpdate

def get_products(db: Session):
    return db.query(Product).all()


def delete_products(db: Session, product_id: str):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

def get_product_by_id(db: Session, product_id: str):
    return db.query(Product).filter(Product.product_id == product_id).first()

def update_product(db: Session, product_id : int, productUpdate)-> Optional[Product] :
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    
    productUpdate = productUpdate.dict()

    # Only update fields that were explicitly provided in the request
    for key, value in productUpdate.items():
        if value is not None:
            setattr(product, key, value)

            

    db.commit()
    db.refresh(product)
    return product

def create_product(db: Session, product):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product_quantity(db: Session, product_id: str, quantity: int):
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    product.quantity = quantity
    db.commit()
    db.refresh(product)
    return product

def get_products_by_category_id(db: Session, category_id: str):
    return db.query(Product).filter(Product.category_id == category_id).all()