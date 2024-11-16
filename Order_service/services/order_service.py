# order_service.py
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from models import Order, OrderItem, OrderCreateSchema, OrderResponseSchema


"""
Following services will be used when:

After user created an shopping card, they will purschase the items in the shopping card.
After user purchased the items, the order will be created and the items will be added to the OrderItem table.

After the order is created, the user can see the order details. 
For example, the user can see the order status, payment status, order date, total price and the items in the order.

And also, when user purchased we will show user one time page in which there is:
At the top, successfull bought message and items that user bought.

"""
class OrderService:
    @staticmethod
    def create_order(order: OrderCreateSchema, db: Session):
        """
            Create a new order and add items to OrderItem table.
            After adding the order and items, fetch the items to include in the response. And then return the response as json object.

            Parameters:
            - order: OrderCreateSchema
                - customer_id: str
                - items: List[OrderItemSchema] : array of OrderItemSchema
                - total_price: DECIMAL
            - db: Session

            Returns:
            - OrderResponseSchema
                - order_id: str
                - customer_id: str
                - total_price: DECIMAL
                - order_date: datetime
                - order_status: str
                - payment_status: str
                - items: List[OrderItemSchema] : array of OrderItemSchema   
        """
        new_order = Order(
            order_id=str(uuid4()),
            customer_id=order.customer_id,
            total_price=order.total_price,
            order_date=datetime.now(),
            order_status="pending",
            payment_status="unpaid"
        )
        
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Add items to OrderItem
        for item in order.items:
            order_item = OrderItem(
                order_item_id=str(uuid4()),
                order_id=new_order.order_id,
                product_id=item.product_id,
                price_at_purchase=item.price_at_purchase,
                quantity=item.quantity
            )
            db.add(order_item)
        
        db.commit()
        
        # Fetch items to include in response
        db.refresh(new_order)
        order_items = db.query(OrderItem).filter(OrderItem.order_id == new_order.order_id).all()

        # return the created order object as json object with the following fields: order_id, customer_id, total_price, order_date, order_status, payment_status, items (a list of OrderItems)
        order_response = OrderResponseSchema(
            order_id=new_order.order_id,
            customer_id=new_order.customer_id,
            total_price=new_order.total_price,
            order_date=new_order.order_date,
            order_status=new_order.order_status,
            payment_status=new_order.payment_status,
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
    def get_order(order_id: str, db: Session):
        """
            Fetch an order by order_id and return the order as json object. (a combination of OrderItems as a json object)

            Parameters:
            - order_id: str
            - db: Session

            Returns:
            - OrderResponseSchema
                - order_id: str
                - customer_id: str
                - total_price: DECIMAL
                - order_date: datetime
                - order_status: str
                - payment_status: str
                - items: List[OrderItemSchema] : array of OrderItemSchema
        """
        # Fetch order
        order = db.query(Order).filter(Order.order_id == order_id).first()
        # If order is not found, return None
        if not order:
            return None
        # Fetch items that has the same order_id as the order
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

        Order_as_json_object = OrderResponseSchema(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total_price=order.total_price,
            order_date=order.order_date,
            order_status=order.order_status,
            payment_status=order.payment_status,
            items=[
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_purchase": item.price_at_purchase
                } for item in order_items
            ]
        )


        return Order_as_json_object

    @staticmethod
    def list_orders_for_customer(customer_id: str, db: Session):
        """
            Fetch all orders for the given customer_id and return a list of orders as json objects.

            Parameters:
            - customer_id: str 
            - db: Session

            Returns:
            - List[OrderResponseSchema]
                - order_id: str
                - customer_id: str
                - total_price: DECIMAL
                - order_date: datetime
                - order_status: str
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
                order_status=order.order_status,
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
    def update_order_status(order_id: str, status: str, db: Session):
        """
            Update the status of the order with the given order_id to the given status.

            Parameters:
            - order_id: str
            - status: str
            - db: Session

            Returns:
            - str : order_status
        """
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return None
        order.order_status = status
        db.commit()
        db.refresh(order)
        return order.order_status
