from fastapi import APIRouter, Depends, HTTPException, Path, status
import uuid
from sqlalchemy.orm import Session
from typing import List
from models.models import Product, ProductCreate, ProductUpdate
from services.services import ProductService
from dbContext import get_db  # This dependency function provides the database session

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[Product])
async def get_all_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str = Path(..., regex=r"^[a-fA-F0-9-]{36}$"), db: Session = Depends(get_db)):
    service = ProductService(db)
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=Product, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    try:
        # Call service to create the product
        return service.create_product(product)
    except ValueError as e:
        # If the service raises a ValueError (e.g., unique constraint failure), return 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except Exception as e:
        # Catch-all for any other exceptions and return a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product."
        )



@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_data: ProductUpdate,
    product_id: str = Path(..., regex=r"^[a-fA-F0-9-]{36}$"),
    db: Session = Depends(get_db)):
    service = ProductService(db)
    
    
    product = service.update_product(product_id, product_data)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    service = ProductService(db)
    success = service.delete_product(str(product_id))  # Ensure product_id is a string
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None