from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from utils.db_utils import get_db
from utils.authentication_utils import verify_user_role, oauth2_scheme
from utils.order_settings import settings
from schemas.refund_cancel_schemas import RefundRequestSchema, RefundResponseSchema, CancelRequestSchema, CancelResponseSchema, RefundSchema, StatusSchema
from services.refund_cancel_service import refund_products, cancel_order_service, get_refund_status


router = APIRouter()


@router.post('/refund', dependencies=[Depends(verify_user_role)])
async def refund_product(refund_request: RefundRequestSchema, db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Refunds products based on the provided refund request.

    Args:
        refund_request (RefundRequestSchema): The schema containing the details of the refund request.
        RefundRequestSchema:
            {
                order_id, str
                product_id_list, List[str]
                reason, Optional[str]
            }
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
        token (str, optional): The OAuth2 token dependency. Defaults to Depends(oauth2_scheme).

    Returns:
        RefundResponseSchema: The schema containing the details of the refund response.
            RefundResponseSchema:
                {
                    order_id, str
                    refunds, List[RefundSchema]
                }
                RefundSchema:
                    {
                        refund_id, str
                        product_id, str
                        status, str
                        refund_amount, float
                    }
        

    """
    result = refund_products(refund_request, db, token)

    if not result:
        raise HTTPException(status_code=404, detail="Refund not created")
    
    return result

@router.get('/refund-status/{order_id}/{product_id}', response_model= RefundSchema, dependencies=[Depends(verify_user_role)])
async def refund_status(order_id:str, product_id:str, db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieves the refund status of a specific order.

    Args:
        order_id (str): The ID of the order to retrieve the refund status for.
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
        token (str, optional): The OAuth2 token dependency. Defaults to Depends(oauth2_scheme).

    Returns:
        RefundResponseSchema: The schema containing the details of the refund response.
            RefundResponseSchema:
                {
                    order_id, str
                    refunds, List[RefundSchema]
                }
                RefundSchema:
                    {
                        product_id, str
                        status, str
                        refund_amount, float
                    }
    """
    refunds = get_refund_status(order_id, product_id, db, token)

    if not refunds:
        raise HTTPException(status_code=404, detail="Refund not found")
    
    return refunds



@router.post('/cancel', response_model = CancelResponseSchema, dependencies=[Depends(verify_user_role)])
async def cancel_order(cancel_request: CancelRequestSchema, db=Depends(get_db), token: str = Depends(oauth2_scheme)):
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



