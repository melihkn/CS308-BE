from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from ..models.models import Product
from ..utils.db_utils import get_db
from ..services.product_service import ProductService

# Create a router for product-related endpoints
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[Dict])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Retrieve all products for display.
    """
    try:
        products = ProductService.get_all_products(db)
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

"""
input example: get request sadece product_id ile çalışıyor

output example:
{
    "name": "Product Name",
    "model": "Product Model",
    "description": "Product Description",
    "quantity": 10,
    "price": 100.0,
    "distributor": "Product Distributor",
    "image_url": "http://image.com/product.jpg"
}
"""
@router.get("/{product_id}", response_model=Dict)
async def get_product_by_id(product_id: str, db: Session = Depends(get_db)):
    """
    Get detailed product information by product ID.
    """
    try:
        product = ProductService.get_product_by_id(product_id, db)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        return product
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.patch("/{product_id}/quantity", response_model=Dict)
async def update_product_quantity(product_id: str, quantity: int, db: Session = Depends(get_db)):
    """
    Update the quantity of a specific product.
    """
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive value")
    
    try:
        updated_product = ProductService.update_product_quantity(product_id, quantity, db)
        if not updated_product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        return updated_product
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.patch("/{product_id}/sold", response_model=Dict)
async def increment_item_sold(product_id: str, quantity_sold: int, db: Session = Depends(get_db)):
    """
    Increment the number of items sold for a specific product.
    """
    if quantity_sold < 1:
        raise HTTPException(status_code=400, detail="Quantity sold must be at least 1")

    try:
        updated_product = ProductService.increment_item_sold(product_id, quantity_sold, db)
        if not updated_product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        return updated_product
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{product_id}/inventory", response_model=Dict)
async def get_product_inventory_status(product_id: str, db: Session = Depends(get_db)):
    """
    Check if a product is in stock and return inventory status.
    """
    try:
        inventory_status = ProductService.get_product_inventory_status(product_id, db)
        if not inventory_status:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        return inventory_status
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
