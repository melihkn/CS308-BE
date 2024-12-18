from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RefundRequestSchema(BaseModel):
    order_id: int = Field(..., description="ID of the order to be refunded")
    product_id_list : List[int] = Field(..., description="List of product IDs to be refunded")
    reason: Optional[str] = Field(None, description="Reason for the refund request")

class RefundSchema(BaseModel):
    refund_id: int = Field(..., description="ID of the refund")
    product_id: int = Field(..., description="ID of the product to be refunded")
    status: str = Field(..., description="Status of the refund")
    refund_amount: float = Field(..., description="Amount to be refunded")

class RefundResponseSchema(BaseModel):
    order_id: int = Field(..., description="ID of the order that was refunded")
    refunds = List[RefundSchema] = Field(..., description="List of refund requests")

class CancelRequestSchema(BaseModel):
    order_id: int = Field(..., description="ID of the order to be canceled")
    reason: Optional[str] = Field(None, description="Reason for the cancellation request")

class CancelResponseSchema(BaseModel):
    order_id: int = Field(..., description="ID of the order that was canceled")
    status: str = Field(..., description="Status of the cancel operation")
    canceled_at: datetime = Field(..., description="Timestamp when the cancellation was processed")