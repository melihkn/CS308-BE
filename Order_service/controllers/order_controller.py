# order_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import OrderCreateSchema, OrderResponseSchema, OrderStatusUpdateSchema
from order_service import OrderService
from utils.db_utils import get_db

router = APIRouter()

@router.post("/create", response_model=OrderResponseSchema)
async def create_order(order: OrderCreateSchema, db: Session = Depends(get_db)):
    """
    Create an order with the given order schema and add it to the database.
    This endpoint returns the created order as a response as a json object with the following fields: order_id, customer_id, total_price, order_date, order_status, payment_status, items (a list of OrderItems)
    """
    try:
        return OrderService.create_order(order, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """
    This endpoint is for getting the order with the given order_id.

    It returns the order as a json object with the following fields: order_id, customer_id, total_price, order_date, order_status, payment_status, items (a list of OrderItems)
    """
    order = OrderService.get_order(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/customer/{customer_id}", response_model=List[OrderResponseSchema])
async def list_orders_for_customer(customer_id: str, db: Session = Depends(get_db)):
    """
    This endpoint is for listing all orders for the given customer_id.

    It returns a list of orders as json objects with the following fields: order_id, customer_id, total_price, order_date, order_status, payment_status, items (a list of OrderItems)
    """
    return OrderService.list_orders_for_customer(customer_id, db)

# this route is for updating the status of the order from pending to completed or cancelled
@router.patch("/{order_id}/status", response_model=dict)
async def update_order_status(order_id: str, status_update: OrderStatusUpdateSchema, db: Session = Depends(get_db)):
    result = OrderService.update_order_status(order_id, status_update.status, db)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated", "order_status": result}
