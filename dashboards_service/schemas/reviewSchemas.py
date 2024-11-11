from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    product_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    review_id: str
    customer_id: str
    product_id: str
    rating: int
    comment: Optional[str] = None
    approval_status: str
    pm_id: Optional[str] = None


class ReviewApprovalUpdate(BaseModel):
    approval_status: str