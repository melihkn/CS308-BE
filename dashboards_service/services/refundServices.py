from sqlalchemy.orm import Session
from models.models import Customer, Order, OrderItem, Product, Refund
from datetime import datetime

from services.EmailService import EmailService

def get_refunds(db: Session):
    return db.query(Refund).all()

def get_refundById(db: Session, refund_id: str):
    refund = db.query(Refund).filter_by(refund_id=refund_id).first()
    return refund

def update_refund_service(db: Session, refund_id: str, refund_data):
    # Refund tablosundan refund_id ile ilgili kaydı bul
    refund = db.query(Refund).filter_by(refund_id=refund_id).first()

    if not refund:
        return None

    # Refund tablosundan refund bilgilerini güncelle
    for key, value in refund_data.dict().items():
        setattr(refund, key, value)

    db.commit()
    db.refresh(refund)

    # Refund ile ilişkili order_id'yi al
    order_id = refund.order_id

    # Orders tablosundan order_id ile ilgili müşteri bilgilerini bul
    order = db.query(Order).filter_by(order_id=order_id).first()

    if not order:
        raise ValueError(f"Order with ID {order_id} not found")

    customer_id = order.customer_id

    # Customers tablosundan müşteri e-postasını bul
    customer = db.query(Customer).filter_by(user_id=customer_id).first()

    if not customer:
        raise ValueError(f"Customer with ID {customer_id} not found")

    customer_email = customer.email

    # Refund bilgilerini e-posta ile gönder
    msg = (
        f"Your refund request for order '{refund.order_id}' with a refund amount of {refund.refund_amount} "
        f"has been {refund.status}."
    )
    subject = "About your refund request"

    if refund.status == "Approved":
        order_item = db.query(OrderItem).filter(OrderItem.order_item_id == refund.order_item_id).first()
        product = db.query(Product).filter(Product.product_id == order_item.product_id).first()

        product.quantity += order_item.quantity

        db.commit()
        db.refresh(product)

    EmailService.send_discount_email(customer_email,subject ,msg)

    return refund
