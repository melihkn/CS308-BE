from sqlalchemy.orm import Session
from datetime import datetime
from models.models import (
    Order,
    OrderItem,
    Product,
    OrderItemCreateSchema, 
    OrderCreateSchema,
    OrderResponseSchema,
    OrderItemResponseSchema,
    OrderStatusUpdateSchema
)
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
import time

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
    def parse_order_date(order_date: str) -> datetime:
        """
        Parse the order date to support both '%Y-%m-%d' and '%Y-%m-%d %H:%M:%S' formats.
        """
        try:
            if " " in order_date:
                return datetime.strptime(order_date, "%Y-%m-%d %H:%M:%S")
            return datetime.strptime(order_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S'.")

    @staticmethod
    def create_order(order_data: OrderCreateSchema, db: Session, max_retries: int = 3):
        """
        This function creates an order with the given data.

        Input:
        - order_data: OrderCreateSchema object containing order details. 
        - db: SQLAlchemy Session object.
        - max_retries: Maximum number of retries in case of database errors.

        Output:
        - Order object if successful.
        """
        retry_count = 0

        while retry_count < max_retries:
            try:
                # Begin transaction
                order_id = str(uuid4())
                print(f"Creating order with ID: {order_id}")
                
                new_order = Order(
                    order_id=order_id,
                    customer_id=order_data.customer_id,
                    total_price=order_data.total_price,
                    order_date=OrderService.parse_order_date(order_data.order_date),
                    payment_status=order_data.payment_status,
                    invoice_link=order_data.invoice_link,
                    order_status=order_data.order_status,
                )
                db.add(new_order)
                print("Order added successfully.")

                # Create order items and update stock
                for item in order_data.items:
                    print(f"Processing item: {item}")

                    product = db.query(Product).filter_by(product_id=item.product_id).first()
                    if not product:
                        raise ValueError(f"Product {item.product_id} not found.")
                    
                    print(f"Product fetched: {product}")
                    if product.quantity < item.quantity:
                        raise ValueError(f"Insufficient stock for product {item.product_id}. "
                                        f"Available: {product.quantity}, Requested: {item.quantity}")

                    # Deduct stock
                    product.quantity -= item.quantity
                    print(f"Stock updated for product {item.product_id}: Remaining {product.quantity}")

                    # Add order item
                    try:
                        new_item = OrderItem(
                            order_id=order_id,
                            product_id=item.product_id,
                            quantity=item.quantity,
                            price_at_purchase=item.price_at_purchase,
                        )
                        db.add(new_item)
                        print(f"OrderItem added: {new_item}")
                    except Exception as e:
                        print(f"Failed to add OrderItem: {str(e)}")
                        raise e

                # Commit the transaction
                db.commit()
                print("Transaction committed successfully.")

                # Reload the order to include relationships
                db.refresh(new_order)
                return new_order

            except ValueError as ve:
                # Rollback and re-raise validation errors
                db.rollback()
                print(f"Validation error: {ve}")
                raise ve

            except SQLAlchemyError as se:
                # Rollback on DB errors
                db.rollback()
                retry_count += 1
                print(f"Database error on retry {retry_count}: {se}")
                if retry_count >= max_retries:
                    raise RuntimeError(f"Database operation failed after {max_retries} retries.") from se

            except Exception as e:
                # Rollback for any other exceptions
                db.rollback()
                print(f"Unexpected error: {e}")
                raise RuntimeError("Unexpected error during order creation.") from e


    @staticmethod
    def get_order(order_id: str, db: Session):
        """
        Retrieve an order by its ID with its associated items.

        Input:
        - order_id: Order ID to retrieve.
        - db: SQLAlchemy Session object.

        Output:
        - Order object if found, None otherwise.
        """
        order = db.query(Order).filter_by(order_id=order_id).first()
        if not order:
            return None

        # Eagerly load related items
        db.refresh(order)
        return order

    @staticmethod
    def list_orders_for_customer(customer_id: str, db: Session):
        """
        List all orders for a specific customer.

        Input:
        - customer_id: Customer ID to retrieve orders for.
        - db: SQLAlchemy Session object.

        Output:
        - List of Order objects for the customer.
        """
        orders = db.query(Order).filter_by(customer_id=customer_id).all()
        for order in orders:
            db.refresh(order)  # Ensure items are loaded
        return orders

    @staticmethod
    def update_order_status(order_id: str, new_status: int, db: Session):
        """
        Update the status of an order.

        Input:
        - order_id: Order ID to update.
        - new_status: New status value.
        - db: SQLAlchemy Session object.

        Output:
        - Updated status value if successful.
        """
        if new_status not in ORDER_STATUS_MAP:
            raise ValueError("Invalid status value.")

        order = db.query(Order).filter_by(order_id=order_id).first()
        if not order:
            return None

        order.order_status = new_status
        db.commit()
        return ORDER_STATUS_MAP[new_status]
