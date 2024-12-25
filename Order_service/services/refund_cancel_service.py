
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from typing import List
from schemas.refund_cancel_schemas import CancelRequestSchema, CancelResponseSchema, RefundRequestSchema, RefundResponseSchema, RefundSchema
from models.models import Customer, Delivery, OrderItem, Order, Refund
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
            print("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        

        # Check if the order and order items exists and belongs to the user
        order = db.query(Order).filter(Order.order_id == refund_request.order_id).first()

        if order.order_status == "CANCELLED" or order.order_status == "REFUNDED":
            print("Order already cancelled or refunded")
            raise HTTPException(status_code=400, detail="Order already cancelled or refunded")
        
        if (datetime.utcnow() - order.order_date).days > 30:
            print("Cannot refund order after 30 days")
            raise HTTPException(status_code=400, detail="Cannot refund order after 30 days")

        if not order:
            print("Order not found")
            raise HTTPException(status_code=404, detail="Order not found")

        
        
        if order.customer_id != user.user_id:
            print("User not authorized to refund this order")
            raise HTTPException(status_code=403, detail="User not authorized to refund this order")
        

        # Create refund objects

        refunds = []
        for item in refund_request.product_id_list:
            order_item = db.query(OrderItem).filter(OrderItem.order_id == order_id, OrderItem.product_id == item).first()

            refund = db.query(Refund).filter(Refund.order_id == order_id, Refund.order_item_id == order_item.order_item_id).first()

            if refund:
                print("Refund already exists for this order item")
                continue
            

            refund = Refund(
                refund_id = str(uuid.uuid1()),
                order_id=order_id,
                order_item_id=order_item.order_item_id,
                request_date = datetime.utcnow(),
                status = "PENDING",
                refund_amount = order_item.price_at_purchase
            )          

            db.add(refund)


        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error processing refunds: {str(e)}")

    

    return {"message": "Refund Requests Successfull Created"}

def get_refund_status(order_id: str, product_id: str, db: Session, token: str) -> RefundResponseSchema:
    """
    Get the refund status of a specific order.
    Args:
        order_id (str): The ID of the order to retrieve the refund status for.
        product_id (str): The ID of the product to retrieve the refund status for.
        db (Session): Database session.
        token (str): JWT token.
    Returns:
        RefundResponseSchema: The schema containing the details of the refund response.
    """

    # Authentication is done in the controller

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")

        user = db.query(Customer).filter(Customer.email == email).first()

        if not user:
            print("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        order = db.query(Order).filter(Order.order_id == order_id).first()

        if not order:
            print("Order not found")
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order.customer_id != user.user_id:
            print("User not authorized to view refund status for this order")
            raise HTTPException(status_code=403, detail="User not authorized to view refund status for this order")

        order_item = db.query(OrderItem).filter(OrderItem.order_id == order_id, OrderItem.product_id == product_id).first()
        if not order_item:
            print("Order item not found")
            raise HTTPException(status_code=404, detail="Order item not found")
        
        refund = db.query(Refund).filter(Refund.order_id == order_id, Refund.order_item_id == order_item.order_item_id).first()
        
        status = None
        if not refund:
            status = "N/A"
        else:
            status = refund.status
        


        return RefundSchema(
            product_id= product_id,
            status= status,
            refund_amount= order_item.price_at_purchase
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing refund status request: {str(e)}")


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
        
        if order.order_status == 4:
            raise HTTPException(status_code=400, detail="Order already cancelled")
        elif order.order_status == 3:
            raise HTTPException(status_code=400, detail="Cannot cancel delivered order")
        elif order.order_status == 2:
            raise HTTPException(status_code=400, detail="Cannot cancel shipped order")
        elif order.order_status == 1:
            raise HTTPException(status_code=400, detail="Cannot cancel refunded order")
        
        order.order_status = 4

        delivery = db.query(Delivery).filter(Delivery.order_id == order.order_id).first()

        delivery.delivery_status = "CANCELLED"

        db.commit()

        return CancelResponseSchema(
            order_id = order.order_id,
            status = 4,
            canceled_at = datetime.utcnow()
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing cancel request: {str(e)}")


    

