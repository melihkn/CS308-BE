from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.orderServices import get_orders, create_order_service, update_order_service, delete_order_service, \
                                   get_orderItems, create_orderItem_service, update_orderItem_service, delete_orderItem_service
from dbContext import get_db
from models.models import Discount
from pydantic import BaseModel, ConfigDict , Field
from typing import List
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
import uuid



router = APIRouter()

class OrderCreate(BaseModel):
    customer_id: str                       # ID of the customer placing the order
    total_price: Decimal                   # Total price of the order
    order_date: datetime = Field(default_factory=datetime.utcnow)  # Order date defaults to current time
    order_status: str                      # Status of the order (e.g., "pending", "completed")
    payment_status: str                    # Payment status (e.g., "paid", "unpaid")
    invoice_link: Optional[str] = None     # Optional link to an invoice

    # Allow arbitrary types like Decimal and datetime
    model_config = ConfigDict(arbitrary_types_allowed=True)

class OrderItemCreate(BaseModel):
    product_id: str                         # ID of the product being ordered
    order_id: str                           # ID of the order to which this item belongs
    price_at_purchase: Decimal              # Price of the product at the time of purchase
    quantity: int = 1                       # Quantity of the product being ordered, default is 1

    model_config = ConfigDict(arbitrary_types_allowed=True)



@router.get("/orders", response_model=List[OrderCreate])
def read_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.post("/orders", response_model=OrderCreate)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order_service(db, order)


@router.get("/orderItems", response_model = List[OrderItemCreate])
def read_orderItems(db: Session = Depends(get_db)):
    return get_orderItems(db)

@router.post("/orderItems", response_model = OrderItemCreate)
def create_orderItem(orderItem: OrderItemCreate, db: Session = Depends(get_db)):
    return create_orderItem_service(db, orderItem)