from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.models import Product 
from utils.db_utils import get_db
from services.product_service import ProductService  # Import the ProductService

# Create a router for product-related endpoints
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# NOT: ALL ENDPOINTS have prefix of /products as we can see above
@router.get("/", response_model=List[dict])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Retrieve all products for display.
    """
    try:
        return ProductService.get_all_products(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=dict)
async def get_product_by_id(product_id: str, db: Session = Depends(get_db)):
    """
    Get detailed product information by product ID.
    """
    try:
        return ProductService.get_product_by_id(product_id, db)
    except HTTPException as e:
        raise e  # Pass through HTTPException with custom status and detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{product_id}/quantity", response_model=dict)
async def update_product_quantity(product_id: str, quantity: int, db: Session = Depends(get_db)):
    """
    Update the quantity of a specific product.
    """
    try:
        return ProductService.update_product_quantity(product_id, quantity, db)
    except HTTPException as e:
        raise e  # Pass through HTTPException with custom status and detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{product_id}/sold", response_model=dict)
async def increment_item_sold(product_id: str, quantity_sold: int, db: Session = Depends(get_db)):
    """
    Increment the number of items sold for a specific product.
    """
    try:
        return ProductService.increment_item_sold(product_id, quantity_sold, db)
    except HTTPException as e:
        raise e  # Pass through HTTPException with custom status and detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}/inventory", response_model=dict)
async def get_product_inventory_status(product_id: str, db: Session = Depends(get_db)):
    """
    Check if a product is in stock and return inventory status.
    """
    try:
        return ProductService.get_product_inventory_status(product_id, db)
    except HTTPException as e:
        raise e  # Pass through HTTPException with custom status and detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


