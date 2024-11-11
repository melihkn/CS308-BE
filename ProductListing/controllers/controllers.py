<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, Path, status, Request
=======
from fastapi import Request,APIRouter, Depends, HTTPException, Path, status
>>>>>>> 52365734bd0b8b702922c978eee19ebecb4f7a90
import uuid
from sqlalchemy.orm import Session
from typing import List
from models.models import Product, ProductCreate, ProductUpdate,ProductDB
from services.services import ProductService
from dbContext import get_db  # This dependency function provides the database session

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[Product])
async def get_all_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()


@router.get("/sorted-by-price", response_model=List[Product])
async def get_products_sorted_by_price(
    order: str = "asc",  # Default is ascending
    db: Session = Depends(get_db)
):
    """
    Get products sorted by price.
    
    :param order: Sorting order, "asc" or "desc".
    """
    service = ProductService(db)
    
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order parameter. Use 'asc' for ascending or 'desc' for descending."
        )
    
    return service.get_products_sorted_by_price(order)



@router.get("/popular", response_model=List[Product])
def get_products_sorted_by_popularity(db: Session = Depends(get_db)):
    service = ProductService(db)
    popular_products = service.get_products_sorted_by_popularity()
    return popular_products


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

<<<<<<< HEAD


=======
>>>>>>> 52365734bd0b8b702922c978eee19ebecb4f7a90
@router.post("/search")
async def search_products(request: Request, db: Session = Depends(get_db)):
    """
    Search products based on the input query from the user.
    """
    data = await request.json()
    query = data.get("query", "").strip()  # Get the search query from the request body

    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

<<<<<<< HEAD
    service = ProductService(db)
    return service.search_product_by_name_description(query)
    # Query the database for matching products
=======
    # Query the database for matching products
    results = db.query(ProductDB).filter(
        (ProductDB.name.ilike(f"%{query}%")) |  # Case-insensitive search for name
        (ProductDB.description.ilike(f"%{query}%"))  # Case-insensitive search for description
    ).all()
    
    # Convert results to a list of dictionaries to return as JSON
    return results
>>>>>>> 52365734bd0b8b702922c978eee19ebecb4f7a90
