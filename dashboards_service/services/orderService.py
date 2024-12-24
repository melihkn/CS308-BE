from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.models import Order, OrderItem, Delivery, Address, Customer, Product
from schemas.orderSchemas import OrderResponseSchema, ProductResponseSchema, OrderUpdateSchema



class OrderService:

    @staticmethod
    def get_orders(db: Session) -> List[OrderResponseSchema]:
        # I understand you but I need to return a list of OrderResponseSchema for the response model
        # I will fix this

        orders = db.query(Order).all()

        response = []

        for order in orders:
            products = []
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
            for item in order_items:
                product = db.query(Product).filter(Product.product_id == item.product_id).first()
                products.append(ProductResponseSchema(
                    product_id = product.product_id,
                    product_name = product.name,
                    quantity = item.quantity,
                    price_at_purchase = item.price_at_purchase
                ))

            delivery = db.query(Delivery).filter(Delivery.delivery_id == order.delivery_id).first()
            address = db.query(Address).filter(Address.address_id == delivery.address_id).first()
            customer = db.query(Customer).filter(Customer.customer_id == order.customer_id).first()

            response.append(OrderResponseSchema(
                delivery_id = delivery.delivery_id,
                order_id = order.order_id,
                customer_id = customer.customer_id,
                price = order.total_price,
                address = address.address,
                status = order.order_status,
                products = products
            ))


        return response
    
    @staticmethod
    def update_order(db: Session, update : OrderUpdateSchema):
        order = db.query(Order).filter(Order.order_id == order.order_id).first()

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        

        if update.status is not None:
            order.order_status = update.status

        if order.price is not None:
            order.total_price = update.price

        if order.address is not None:
            order.address = update.address

        db.commit()
        db.refresh(order)

        # I think I dont have to return this because I have all the data in the frontend. only the status code is enough ?? I am asking to you
        return {'message': 'Order updated successfully'}

