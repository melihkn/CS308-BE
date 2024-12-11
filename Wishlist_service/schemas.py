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
