from pydantic import BaseModel
from typing import Optional

class WishlistCreate(BaseModel):
    name: Optional[str] = None
    customer_id: str
    wishlist_status: str

class WishlistResponse(BaseModel):
    wishlist_id: str
    name: Optional[str]
    customer_id: str
    wishlist_status: str

    class Config:
        orm_mode = True

class WishlistItemCreate(BaseModel):
    wishlist_id: str # wishlist_id is to put the item correctly to the wanted wishlist 
    product_id: str

# this is the response model for the wishlist item 
class WishlistItemResponse(BaseModel):
    wishlist_item_id: str
    wishlist_id: str
    product_id: str

    class Config:
        orm_mode = True