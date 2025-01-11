from pydantic import BaseModel
from typing import Optional, List

class ProductResponseSchema(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price_at_purchase: float
    image_url: str

class OrderResponseSchema(BaseModel):
    id: str
    order_id: str
    customer_id: str
    price: float
    address: str
    status: int
    products : List[ProductResponseSchema]


class OrderUpdateSchema(BaseModel):
    order_id: str
    status: int

