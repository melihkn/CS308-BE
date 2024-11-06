from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, services, models
from ..dbContext import get_db, get_current_user
#from ..auth import get_current_active_product_manager

router = APIRouter(
    prefix="/product_manager",
    tags=["products"],
    #dependencies=[Depends(get_current_active_product_manager)]
)

@router.post("/", response_model = schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Optional: Validate category_id, pm_id, sm_id exist
    return services.product.create_product(db, product)

@router.get("/", response_model=List[schemas.ProductOut])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = services.product.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.ProductOut)
def read_product(product_id: str, db: Session = Depends(get_db)):
    db_product = services.product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: str, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    updated_product = services.product.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", response_model=schemas.ProductOut)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    deleted_product = services.product.delete_product(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product