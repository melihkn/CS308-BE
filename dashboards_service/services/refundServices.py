from sqlalchemy.orm import Session
from models.models import Order, OrderItem, Refund
from datetime import datetime


def get_refunds(db: Session):
    return db.query(Refund).all()

def get_refundById(db: Session, refund_id: str):
    refund = db.query(Refund).filter_by(refund_id=refund_id).first()
    return refund

def update_refund_service(db: Session, refund_id: str, refund_data):
    refund = db.query(Refund).filter_by(refund_id=refund_id).first()
    if refund:
        for key, value in refund_data.dict().items():
            setattr(refund, key, value)
        db.commit()
        db.refresh(refund)
    return refund
