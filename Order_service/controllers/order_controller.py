from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import OrderCreateSchema, OrderResponseSchema, OrderStatusUpdateSchema, RefundResponseSchema
from services.order_service import OrderService
from utils.db_utils import get_db

router = APIRouter()

@router.post("/create", response_model=OrderResponseSchema)
async def create_order(order: OrderCreateSchema, db: Session = Depends(get_db)):
    """
    Create an order with the given order schema and add it to the database.
    """
    try:
        return OrderService.create_order(order, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """
    Get the order with the given order_id.

    This endpoint returns the order as a JSON object with the following fields: 
    order_id, customer_id, total_price, order_date, order_status, payment_status, items (a list of OrderItems)
    """
    order = OrderService.get_order(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/customer/{customer_id}", response_model=List[OrderResponseSchema])
async def list_orders_for_customer(customer_id: str, db: Session = Depends(get_db)):
    """
    List all orders for the given customer_id.

    This endpoint returns a list of orders as JSON objects with the following fields: 
    order_id, customer_id, total_price, order_date, order_status, payment_status, items (a list of OrderItems)
    """
    return OrderService.list_orders_for_customer(customer_id, db)

@router.patch("/{order_id}/status", response_model=dict)
async def update_order_status(order_id: str, status_update: OrderStatusUpdateSchema, db: Session = Depends(get_db)):
    """
    Update the status of an order.

    This endpoint updates the status of the order with the given order_id. 
    The status must be an integer (e.g., 0 for Preparing, 1 for Shipped, etc.).

    Parameters:
    - order_id: The ID of the order to update.
    - status_update: The new status of the order as an integer.

    Returns:
    - A JSON object with a message and the updated order status.
    """
    try:
        result = OrderService.update_order_status(order_id, status_update.status, db)
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order status updated", "order_status": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{order_id}/return/{product_id}", response_model=RefundResponseSchema)
async def return_product(
    order_id: str, product_id: str, return_quantity: int, db: Session = Depends(get_db)
):
    """
    Process a return for a specific product in an order.

    Parameters:
    - order_id: str - The ID of the order.
    - product_id: str - The ID of the product to be returned.
    - return_quantity: int - The quantity to be returned.

    Returns:
    - RefundResponseSchema: A JSON response with refund details.
    """
    try:
        result = OrderService.return_product(order_id, product_id, return_quantity, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
