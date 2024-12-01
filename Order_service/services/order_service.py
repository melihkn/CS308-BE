# order_service.py
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from Order_service.models.models import Order, OrderItem, Product, Refund, OrderCreateSchema, OrderResponseSchema, OrderItemSchema
"""
Following services will be used when:

After user creates a shopping cart, they will purchase the items in the shopping cart.
After user purchases the items, the order will be created and the items will be added to the OrderItem table.

After the order is created, the user can see the order details. 
For example, the user can see the order status, payment status, order date, total price, and the items in the order.

And also, when a user purchases, we will show a one-time page with:
At the top, a success message and the items that the user bought.
"""


ORDER_STATUS_MAP = {
    0: "pending",
    1: "processing",
    2: "shipped",
    3: "delivered",
    4: "cancelled",
    5: "returned"
}

class OrderService:
    @staticmethod
    def create_order(order: OrderCreateSchema, db: Session):
        """
        Create a new order and associated items, and return the created order details.
        """
        # Check stock and create the order
        for item in order.items:
            product = db.query(Product).filter(Product.product_id == item.product_id).first()
            if product.quantity < item.quantity:
                raise ValueError(f"Insufficient stock for product {product.name}")

        new_order = Order(
            order_id=str(uuid4()),
            customer_id=order.customer_id,
            total_price=order.total_price,
            order_date=datetime.utcnow(),
            order_status=0,  # Default status: pending
            payment_status="unpaid"  # Default payment status
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Add items to the order and update stock
        for item in order.items:
            order_item = OrderItem(
                order_item_id=str(uuid4()),
                order_id=new_order.order_id,
                product_id=item.product_id,
                price_at_purchase=item.price_at_purchase,
                quantity=item.quantity
            )
            db.add(order_item)
            product.quantity -= item.quantity  # Update stock
        db.commit()
        db.refresh(new_order)
        return new_order

    @staticmethod
    def get_order(order_id: str, db: Session):
        """
        Fetch an order by order_id and return the order as a JSON object.

        Parameters:
        - order_id: str
        - db: Session

        Returns:
        - OrderResponseSchema
            - order_id: str
            - customer_id: str
            - total_price: DECIMAL
            - order_date: datetime
            - order_status: int
            - payment_status: str
            - items: List[OrderItemSchema] : array of OrderItemSchema
        """
        # Fetch order
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return None

        # Fetch items for the order
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

        # Return order as JSON
        order_response = OrderResponseSchema(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total_price=order.total_price,
            order_date=order.order_date,
            order_status=order.order_status,  # Return integer status
            payment_status=order.payment_status,
            items=[
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_purchase": item.price_at_purchase
                } for item in order_items
            ]
        )

        return order_response

    @staticmethod
    def list_orders_for_customer(customer_id: str, db: Session):
        """
        Fetch all orders for the given customer_id and return a list of orders as JSON objects.

        Parameters:
        - customer_id: str 
        - db: Session

        Returns:
        - List[OrderResponseSchema]
            - order_id: str
            - customer_id: str
            - total_price: DECIMAL
            - order_date: datetime
            - order_status: int
            - payment_status: str
            - items: List[OrderItemSchema] : array of OrderItemSchema
        """
        orders = db.query(Order).filter(Order.customer_id == customer_id).all()
        response = []

        for order in orders:
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
            response.append(OrderResponseSchema(
                order_id=order.order_id,
                customer_id=order.customer_id,
                total_price=order.total_price,
                order_date=order.order_date,
                order_status=order.order_status,  # Return integer status
                payment_status=order.payment_status,
                items=[
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price_at_purchase": item.price_at_purchase
                    } for item in order_items
                ]
            ))
        return response

    @staticmethod
    def update_order_status(order_id: str, status: int, db: Session):
        """
        Update the status of the order with the given order_id to the given status.

        Parameters:
        - order_id: str
        - status: int
        - db: Session

        Returns:
        - int : order_status
        """
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return None

        if status not in ORDER_STATUS_MAP:
            raise ValueError(f"Invalid status: {status}")

        order.order_status = status  # Set status as integer
        db.commit()
        db.refresh(order)
        return order.order_status

    @staticmethod
    def return_product(order_id: str, product_id: str, return_quantity: int, db: Session):
        """
        Handle product return and update stock.
        """
        order_item = db.query(OrderItem).filter(OrderItem.order_id == order_id, OrderItem.product_id == product_id).first()
        if not order_item:
            raise ValueError("Order item not found")

        product = db.query(Product).filter(Product.product_id == product_id).first()
        product.quantity += return_quantity  # Add returned quantity back to stock
        db.delete(order_item)
        db.commit()
        return {"message": "Product returned and stock updated"}

