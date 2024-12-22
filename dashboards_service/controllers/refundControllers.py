from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dbContext import get_db
from services.refundServices import get_refunds, update_refund_service, get_refundById

from dependencies import verify_sm_role
from dependencies import oauth2_scheme
from dbContext import get_db
from jose import jwt
from settings import settings

router = router = APIRouter(prefix="/refunds", tags=["Refunds"])

class RefundReadSchema(BaseModel):
    refund_id: str
    order_id: str
    order_item_id: str
    request_date: datetime
    status: str
    refund_amount: float

    class Config:
        orm_mode = True

class RefundStatusUpdateSchema(BaseModel):
    status: str

    class Config:
        orm_mode = True



#dependencies=[Depends(verify_sm_role)]
#token: str = Depends(oauth2_scheme)
@router.get("/", response_model=List[RefundReadSchema])
def get_all_refunds_controller(db: Session = Depends(get_db)):
    refunds = get_refunds(db)
    if not refunds:
        raise HTTPException(status_code=404, detail="No refunds found")
    return refunds

# GET: Belirli bir Refund ID ile Refund Getir
@router.get("/{refund_id}", response_model=RefundReadSchema)
def get_refund_by_id_controller(refund_id: str, db: Session = Depends(get_db)):
    refund = get_refundById(db, refund_id)
    if not refund:
        raise HTTPException(status_code=404, detail=f"Refund with ID {refund_id} not found")
    return refund


@router.put("/{refund_id}/Approved", response_model=RefundReadSchema)
def approve_refund(refund_id: str, db: Session = Depends(get_db)):
    """Refund statusunu 'Approved' olarak güncelle."""
    # RefundStatusUpdateSchema kullanılarak body oluşturuluyor
    refund_data = RefundStatusUpdateSchema(status="Approved")
    refund = update_refund_service(db, refund_id, refund_data)
    if not refund:
        raise HTTPException(status_code=404, detail=f"Refund with ID {refund_id} not found")
    return refund


@router.put("/{refund_id}/Rejected", response_model=RefundReadSchema)
def reject_refund(refund_id: str, db: Session = Depends(get_db)):
    """Refund statusunu 'Declined' olarak güncelle."""
    # RefundStatusUpdateSchema kullanılarak body oluşturuluyor
    refund_data = RefundStatusUpdateSchema(status="Declined")
    refund = update_refund_service(db, refund_id, refund_data)
    if not refund:
        raise HTTPException(status_code=404, detail=f"Refund with ID {refund_id} not found")
    return refund