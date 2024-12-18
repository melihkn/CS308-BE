from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from utils.db_utils import get_db
from utils.authentication_utils import verify_user_role, oauth2_scheme
from utils.order_settings import settings
from schemas.refund_cancel_schemas import RefundRequestSchema, RefundResponseSchema, CancelRequestSchema, CancelResponseSchema
from services.refund_cancel_service import refund_products, cancel_order_service


router = APIRouter('/')


@router.post('/refund', response_model=RefundRequestSchema, dependencies=[Depends(verify_user_role)])
async def refund_product(refund_request: RefundRequestSchema, db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Refunds products based on the provided refund request.

    Args:
        refund_request (RefundRequestSchema): The schema containing the details of the refund request.
        RefundRequestSchema:
            {
                order_id, int
                product_id_list, List[int]
                reason, Optional[str]
            }
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
        token (str, optional): The OAuth2 token dependency. Defaults to Depends(oauth2_scheme).

    Returns:
        RefundResponseSchema: The schema containing the details of the refund response.
            RefundResponseSchema:
                {
                    order_id, int
                    refunds, List[RefundSchema]
                }
                RefundSchema:
                    {
                        refund_id, int
                        product_id, int
                        status, str
                        refund_amount, float
                    }
        

    """
    refunds = refund_products(refund_request, db, token)

    if not refunds:
        raise HTTPException(status_code=404, detail="Refund not created")
    
    return refunds


@router.post('/cancel', response_model = [CancelResponseSchema], dependencies=[Depends(verify_user_role)])
def cancel_order(cancel_request: CancelRequestSchema, db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> CancelResponseSchema:
    """
    Cancels an order based on the provided order ID and cancel request.

    Args:
        cancel_request (CancelRequestSchema): The schema containing the details of the cancel request.
            CancelRequestSchema:
                {
                    order_id, int
                    reason, Optional[str]
                }
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
        token (str, optional): The OAuth2 token dependency. Defaults to Depends(oauth2_scheme).

    Returns:
        CancelResponseSchema: The schema containing the details of the cancel response.
            CancelResponseSchema:
                {
                    order_id, int
                    status, str
                    canceled_at, datetime
                }
    """
    
    result = cancel_order_service(cancel_request, db, token)

    return result



