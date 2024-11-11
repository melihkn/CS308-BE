from sqlalchemy.orm import Session
from models.models import Order, OrderItem
from datetime import datetime

def get_orders(db: Session):
    return db.query(Order).all()

def create_order_service(db: Session, order_data):
    order = Order(**order_data.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def update_order_service(db: Session, order_id: str, order_data):
    order = db.query(Order).filter_by(order_id=order_id).first()
    if order:
        for key, value in order_data.dict().items():
            setattr(order, key, value)
        db.commit()
        db.refresh(order)
    return order

def delete_order_service(db: Session, order_id: str):
    order = db.query(Order).filter_by(order_id=order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return {"message": "order deleted successfully"}


def get_orderItems(db: Session):
    return db.query(OrderItem).all()

def create_orderItem_service(db: Session, orderItem_data):
    orderItem = OrderItem(**orderItem_data.dict())
    db.add(orderItem)
    db.commit()
    db.refresh(orderItem)
    return orderItem

def update_orderItem_service(db: Session, orderItem_id: str, orderItem_data):
    orderItem = db.query(OrderItem).filter_by(orderItem_id=orderItem_id).first()
    if orderItem:
        for key, value in orderItem_data.dict().items():
            setattr(orderItem, key, value)
        db.commit()
        db.refresh(orderItem)
    return orderItem

def delete_orderItem_service(db: Session, orderItem_id: str):
    orderItem = db.query(OrderItem).filter_by(orderItem_id=orderItem_id).first()
    if orderItem:
        db.delete(orderItem)
        db.commit()
    return {"message": "orderItem deleted successfully"}
