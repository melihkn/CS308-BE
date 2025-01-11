from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    product_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    review_id: str
    image_url: Optional[str] = None
    customer_id: str
    customer_name: str
    product_name: str
    product_id: str
    rating: int
    comment: Optional[str] = None
    approval_status: str


class ReviewApprovalUpdate(BaseModel):
    approval_status: str