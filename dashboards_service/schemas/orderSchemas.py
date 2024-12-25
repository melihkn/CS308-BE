from pydantic import BaseModel
from typing import Optional, List

class ProductResponseSchema(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price_at_purchase: float

class OrderResponseSchema(BaseModel):
    delivery_id: str
    order_id: str
    price: float
    address: str
    status: int
    products : List[ProductResponseSchema]


class OrderUpdateSchema(BaseModel):
    order_id: str
    status: Optional[int] = None

