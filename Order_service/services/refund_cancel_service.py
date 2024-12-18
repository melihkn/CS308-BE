
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from Order_service.schemas.refund_cancel_schemas import CancelRequestSchema, CancelResponseSchema, RefundRequestSchema, RefundResponseSchema
from models.models import Customer, OrderItem, Order, Refund
from utils.db_utils import get_db
from utils.order_settings import settings
from fastapi import HTTPException
from jose import JWTError, jwt


def refund_products(refund_request: RefundRequestSchema, db: Session, token: str) -> RefundResponseSchema:
    """
    Create refund object and sales manager will apply or not according to the reason and amount. So just create the refund object and return the refund object.
    Args:
        refund_request (RefundRequestSchema): Refund Requests.
        db (Session): Database session.
        token (str): JWT token.
    Returns:
        List[RefundResponseSchema]: List of refund responses.
    """

    # Authentication is done in the controller

    try:

        # Decode the JWT token to get the user email
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")

        order_id = refund_request.order_id

        # Get the user ID from the email
        user = db.query(Customer).filter(Customer.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        

        # Check if the order and order items exists and belongs to the user
        order = db.query(Order).filter(Order.order_id == refund_request[0].order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        
        
        if order.customer_id != user.user_id:
            raise HTTPException(status_code=403, detail="User not authorized to refund this order")
        

        # Create refund objects

        refunds = []
        for item in refund_request.product_id_list:
            order_item = db.query(OrderItem).filter(OrderItem.order_id == order_id, OrderItem.product_id == item).first()
            if not order_item:
                raise HTTPException(status_code=404, detail="Order item not found")

            refund = Refund(
                order_id=order_id,
                order_item_id=order_item.order_item_id,
                request_date = datetime.utcnow(),
                status = "PENDING",
                refund_amount = order_item.price_at_purchase
            )          

            refunds.append(refund)

    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error processing refunds: {str(e)}")


    try:
        db.add_all(refunds)
        db.commit()
        ids = [refund.refund_id for refund in refunds]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error processing refunds")
    

    return RefundResponseSchema(
        order_id = order_id,
        refunds = [
            {
                "refund_id": refund.refund_id,
                "product_id": db.query(OrderItem).filter(OrderItem.order_item_id == refund.order_item_id).first().product_id,
                "status": refund.status,
                "refund_amount": refund.refund_amount
            }
            for refund in refunds
        ]
    )

def cancel_order_service(cancel_request: CancelRequestSchema, db: Session, token: str) -> CancelResponseSchema:
    
    # Authentication is done in the controller

    # Check if the user and order exists

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")

        user = db.query(Customer).filter(Customer.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        order = db.query(Order).filter(Order.order_id == cancel_request.order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.customer_id != user.user_id:
            raise HTTPException(status_code=403, detail="User not authorized to cancel this order")
        
        order.order_status = "CANCELLED"

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing cancel request: {str(e)}")


    

