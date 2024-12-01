from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import (
    OrderCreateSchema,
    OrderResponseSchema,
    OrderStatusUpdateSchema
)
from services.order_service import OrderService
from utils.db_utils import get_db

router = APIRouter()


"""
input is sth like:
{
    "customer_id": "c1",
    "total_price": 100.0,
    "order_date": "2021-10-10",
    "payment_status": "paid",
    "invoice_link": "http://invoice.com",
    "order_status": 0,
    "items": [
        {
            "product_id": "p1",
            "quantity": 2,
            "price_at_purchase": 50.0
        },
        {
            "product_id": "p2",
            "quantity": 1,
            "price_at_purchase": 50.0
        }
    ]
}

output is sth like:
{
    "order_id": "o1",
    "customer_id": "c1",
    "total_price": 100.0,
    "order_date": "2021-10-10 00:00:00",
    "payment_status": "paid",
    "invoice_link": "http://invoice.com",
    "order_status": 0,
    "items": [
        {
            "product_id": "p1",  
            "quantity": 2,
            "price": 50.0
        },

        {
            "product_id": "p2",
            "quantity": 1,
            "price": 50.0
        }
    ]
}
"""
@router.post("/create", response_model=OrderResponseSchema)
async def create_order(order: OrderCreateSchema, db: Session = Depends(get_db)):
    try:
        new_order = OrderService.create_order(order, db)
        
        # Convert the response to match the schema
        return OrderResponseSchema(
            order_id=new_order.order_id,
            customer_id=new_order.customer_id,
            total_price=new_order.total_price,
            order_date=new_order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            payment_status=new_order.payment_status,
            invoice_link=new_order.invoice_link,
            order_status=new_order.order_status,
            items=[
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price_at_purchase,
                }
                for item in new_order.order_items
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
input is order_id
output is the order with the given order_id in the following format:
{
    "order_id": "o1",
    "customer_id": "c1",
    "total_price": 100.0,
    "order_date": "2021-10-10 00:00:00",
    "payment_status": "paid",
    "invoice_link": "http://invoice.com",
    "order_status": 0,
    "items": [
        {
            "product_id": "p1",
            "quantity": 2,
            "price": 50.0
        },

        {
            "product_id": "p2",
            "quantity": 1,
            "price": 50.0
        }
    ]
}
"""
@router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    order = OrderService.get_order(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Convert order to response schema
    return OrderResponseSchema(
        order_id=order.order_id,
        customer_id=order.customer_id,
        total_price=order.total_price,
        order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
        payment_status=order.payment_status,
        invoice_link=order.invoice_link,
        order_status=order.order_status,
        items=[
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price_at_purchase,
            }
            for item in order.order_items
        ]
    )

"""
Returns all orders for a given customer.
input is customer_id

output is a list of orders in the following format:
[
    {
        "order_id": "o1",
        "customer_id": "c1",
        "total_price": 100.0,
        "order_date": "2021-10-10 00:00:00",
        "payment_status": "paid",
        "invoice_link": "http://invoice.com",
        "order_status": 0,
        "items": [
            {
                "product_id": "p1",
                "quantity": 2,
                "price": 50.0
            },

            {
                "product_id": "p2",
                "quantity": 1,
                "price": 50.0
            }
        ]
    },
    ...
]
"""
@router.get("/customer/{customer_id}", response_model=List[OrderResponseSchema])
async def list_orders_for_customer(customer_id: str, db: Session = Depends(get_db)):
    try:
        orders = OrderService.list_orders_for_customer(customer_id, db)
        return [
            OrderResponseSchema(
                order_id=order.order_id,
                customer_id=order.customer_id,
                total_price=order.total_price,
                order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                payment_status=order.payment_status,
                invoice_link=order.invoice_link,
                order_status=order.order_status,
                items=[
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price": item.price_at_purchase,
                    }
                    for item in order.order_items
                ]
            )
            for order in orders
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
input is sth like:
{
    "status": 1
}

output is sth like:
{
    "message": "Order status updated",
    "order_status": 1 -> it returns the updated status of the order in the string format
}
"""
@router.patch("/{order_id}/status", response_model=dict)
async def update_order_status(order_id: str, status_update: OrderStatusUpdateSchema, db: Session = Depends(get_db)):
    try:
        updated_status = OrderService.update_order_status(order_id, status_update.status, db)
        if not updated_status:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order status updated", "order_status": updated_status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


