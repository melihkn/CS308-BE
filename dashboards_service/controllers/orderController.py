from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas.orderSchemas import OrderResponseSchema, ProductResponseSchema, OrderUpdateSchema
from dbContext import get_db
from dependencies import verify_pm_role, oauth2_scheme
from services.orderService import OrderService


router = APIRouter('/orders')


@router.get('/', response_model=List[OrderResponseSchema], dependencies=[Depends(verify_pm_role)])
def get_orders(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return OrderService.get_orders(db)


@router.put('/', dependencies=[Depends(verify_pm_role)])
def update_order(updates : OrderUpdateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return OrderService.update_order(db, updates)