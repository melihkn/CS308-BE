from sqlalchemy.orm import Session
from models.models import Discount
from datetime import datetime

def get_discounts(db: Session):
    return db.query(Discount).all()

def create_discount_service(db: Session, discount_data):
    discount = Discount(**discount_data.dict())
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

def update_discount_service(db: Session, discount_id: str, discount_data):
    discount = db.query(Discount).filter_by(discount_id=discount_id).first()
    if discount:
        for key, value in discount_data.dict().items():
            setattr(discount, key, value)
        db.commit()
        db.refresh(discount)
    return discount

def delete_discount_service(db: Session, discount_id: str):
    discount = db.query(Discount).filter_by(discount_id=discount_id).first()
    if discount:
        db.delete(discount)
        db.commit()
    return {"message": "Discount deleted successfully"}

