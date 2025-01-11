from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.models import Order, OrderItem, Delivery, Address, Customer, Product
from schemas.orderSchemas import OrderResponseSchema, ProductResponseSchema, OrderUpdateSchema


status_map = {
    0: 'PENDING',
    1: 'PROCESSING',
    2: 'SHIPPED',
    3: 'APPROVED',
    4: 'CANCELLED',
}


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
                    price_at_purchase = item.price_at_purchase,
                    image_url = product.image_url
                ))

            delivery = db.query(Delivery).filter(Delivery.order_id == order.order_id).first()
            address = None
            if delivery:
                address = db.query(Address).filter(Address.customer_adres_id == delivery.addres_id).first()
            customer = db.query(Customer).filter(Customer.user_id == order.customer_id).first()

            response.append(OrderResponseSchema(
                id = delivery.delivery_id,
                order_id = order.order_id,
                customer_id = customer.user_id,
                price = order.total_price,
                address = address.address,
                status = order.order_status,
                products = products
            ))

        print(response)

        return response
    
    @staticmethod
    def update_order(db: Session, update : OrderUpdateSchema):
        order = db.query(Order).filter(Order.order_id == update.order_id).first()

        print(order)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        if update.status is not None:
            order.order_status = update.status

        delivery = db.query(Delivery).filter(Delivery.order_id == order.order_id).first()

        if delivery is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery not found"
            )
        
        delivery.delivery_status = status_map[update.status]

        db.commit()
        db.refresh(order)

        # I think I dont have to return this because I have all the data in the frontend. only the status code is enough ?? I am asking to you
        return {'message': 'Order updated successfully'}

