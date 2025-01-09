import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import (
    OrderCreateSchema,
    OrderResponseSchema,
    OrderStatusUpdateSchema,
    Address,
    Delivery
)
from services.order_service import OrderService
from utils.db_utils import get_db
from utils.authentication_utils import verify_user_role, oauth2_scheme
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()


"""
OrderCreate schema:
class OrderCreateSchema(BaseModel):
    order_id: str
    customer_id: str
    total_price: float
    order_date: str
    order_address : str
    order_address_type: str #Home, work etc.
    order_address_name: Optional[str]
    payment_status: str
    invoice_link: Optional[str]
    order_status: int
    items: List[OrderItemResponseSchema]

OrderResponse schema:
class OrderResponseSchema(BaseModel):
    order_id: str
    customer_id: str
    total_price: float
    order_date: str
    order_address : Optional[str]
    order_address_type: Optional[str]
    order_address_name: Optional[str]
    payment_status: str
    invoice_link: Optional[str]
    order_status: int
    items: List[OrderItemResponseSchema]

"""

"""
input is sth like:
{
    "customer_id": "c1",
    "total_price": 100.0,
    "order_date": "2021-10-10",
    "order_adress": "Tuzla Istanbul Turkey",
    "order_adress_type": "Home",
    "order_address_name": "Home",
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
    "order_address": "Tuzla Istanbul Turkey",
    "order_address_type": "Home",
    "order_address_name": "Home",
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
@router.post("/create", response_model=OrderResponseSchema, dependencies=[Depends(verify_user_role)])
async def create_order(order: OrderCreateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # for debugging: print(order)
        # Create the order
        new_order = OrderService.create_order(order, db)

        # find the related delivery object using the order_id column in the delivery table
        delivery = db.query(Delivery).filter(Delivery.order_id == new_order.order_id).first()

        #if not delivery:
            #raise HTTPException(status_code=404, detail="Delivery not found for the order")

        address = None
        # for the previously added order with no delivery and address, return None for the address fields
        if not delivery:
            address = None
        else:
            address = db.query(Address).filter(Address.customer_adres_id == delivery.addres_id).first()

        # find the related address object using the addres_id column in the delivery table
        address = db.query(Address).filter(Address.customer_adres_id == delivery.addres_id).first()

        # then, create the order response schema using the fields of address object
        return OrderResponseSchema(
            order_id=new_order.order_id,
            customer_id=new_order.customer_id,
            total_price=new_order.total_price,
            order_date=new_order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            order_address= address.address if address else None,
            order_address_type= address.type if address else None,
            order_address_name= address.name if address else None,
            payment_status=new_order.payment_status,
            invoice_link=new_order.invoice_link,  # Include the invoice link in the response
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
    "order_address": "Tuzla Istanbul Turkey",
    "order_address_type": "Home",
    "order_address_name": "Home",
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
@router.get("/{order_id}", response_model=OrderResponseSchema, dependencies=[Depends(verify_user_role)])
async def get_order(order_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    order = OrderService.get_order(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # find the related delivery object using the order_id column in the delivery table
    delivery = db.query(Delivery).filter(Delivery.order_id == order.order_id).first()

    address = None # for the previously added order with no delivery and address, return None for the address fields
    if delivery:
        # find the related address object using the addres_id column in the delivery table
        address = db.query(Address).filter(Address.customer_adres_id == delivery.addres_id).first()

    order_in_response_format = OrderResponseSchema(
        order_id=order.order_id,
        customer_id=order.customer_id,
        total_price=order.total_price,
        order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
        order_address= address.address if address else None,
        order_address_name= address.name if address else None,
        order_address_type= address.type if address else None,
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
    return order_in_response_format


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
        "order_address": "Tuzla Istanbul Turkey",
        "order_address_type": "Home",
        "order_address_name": "Home",
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
@router.get("/customer/{customer_id}", response_model=List[OrderResponseSchema], dependencies=[Depends(verify_user_role)])
async def list_orders_for_customer(customer_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        orders = OrderService.list_orders_for_customer(customer_id, db)

        orders_in_correct_format = []

        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for the customer")

        for order in orders:

            # find the related delivery object using the order_id column in the delivery table
            delivery = db.query(Delivery).filter(Delivery.order_id == order.order_id).first()

            #if not delivery:
                #raise HTTPException(status_code=404, detail="Delivery not found for the order with the id: " + order.order_id)
            
            address = None
            # for the previously added order with no delivery and address, return None for the address fields
            if not delivery:
                address = None
            else:
                # find the related address object using the addres_id column in the delivery table
                address = db.query(Address).filter(Address.customer_adres_id == delivery.addres_id).first()

            current_order_in_correct_format = OrderResponseSchema(
                order_id=order.order_id,
                customer_id=order.customer_id,
                total_price=order.total_price,
                order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                order_address = address.address if address else None,
                order_address_type= address.type if address else None,
                order_address_name= address.name if address else None,
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
            orders_in_correct_format.append(current_order_in_correct_format)
        
        return orders_in_correct_format
    
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
@router.patch("/{order_id}/status", response_model=dict, dependencies=[Depends(verify_user_role)])
async def update_order_status(order_id: str, status_update: OrderStatusUpdateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        updated_status = OrderService.update_order_status(order_id, status_update.status, db)
        if not updated_status:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order status updated", "order_status": updated_status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



from fastapi.responses import FileResponse

"""
port 8004:
input url: api/orders/invoice/ORDER_ID

output is the invoice PDF file for the given order ID.
"""
@router.get("/invoice/{order_id}", response_class=FileResponse)
async def get_invoice(order_id: str, db: Session = Depends(get_db)):
    """
    Serve the invoice PDF for the given order ID.
    """
    # Fetch the order details
    order = OrderService.get_order(order_id, db)

    # Get the current directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the invoices directory relative to this file
    invoices_dir = os.path.join(current_dir, "../invoices")

    # Ensure the invoices directory exists
    os.makedirs(invoices_dir, exist_ok=True)

    # Define the full path for the invoice file
    invoice_path = os.path.join(invoices_dir, f"INV-{order.order_id}.pdf")
    if not order or not order.invoice_link:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if not os.path.exists(invoice_path):
        raise HTTPException(status_code=404, detail="Invoice file not found")

    # Return the PDF file
    return FileResponse(
        invoice_path,  # Path to the invoice PDF
        media_type="application/pdf",
        filename=f"Invoice-{order_id}.pdf"  # Name of the file when downloaded
    )
