from pydantic import BaseModel, Field
from typing import Optional

class Review_Request(BaseModel):
    product_id: str  # Required field
    rating: Optional[int] = Field(..., ge=1, le=5)  # Optional field
    comment: Optional[str] = None  # Optional field

class Get_Review_Response(BaseModel):
    product_id: str  # Required field

class Review_Response(BaseModel):
    review_id: str  # Required field
    product_id: str  # Required field
    rating: int  # Required field
    comment: Optional[str] = None  # Optional field
