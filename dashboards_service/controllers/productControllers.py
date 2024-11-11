from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from dbContext import get_db
from services import products
from dependencies import verify_pm_role, oauth2_scheme

router = APIRouter(prefix="/products", tags=["Products"])

# Pydantic Model for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    pm_id: Optional[str] = None
    sm_id: Optional[str] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = None
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None



# Pydantic Model for creating a product
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    model: str = Field(..., description="Product model")
    description: Optional[str] = Field(None, description="Product description")
    category_id: Optional[int] = None
    item_sold: Optional[int] = 0
    price : Optional[float] = 0.0
    cost : Optional[float] = 0.0
    serial_number: str = Field(..., description="Product serial number")
    quantity: int = Field(..., ge=0, description="Available quantity")
    warranty_status: Optional[int] = None
    distributor: Optional[str] = None
    image_url: Optional[str] = None

class ProductResponse(ProductCreate):
    product_id: str

@router.post("/", response_model=ProductResponse, dependencies=[Depends(verify_pm_role)])
async def create_product(productCreate: ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_product = products.create_product(db, productCreate)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

#, dependencies=[Depends(verify_pm_role)] , token: str = Depends(oauth2_scheme)
@router.get("/", response_model=List[ProductResponse], dependencies=[Depends(verify_pm_role)])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    productsList = products.get_products(db)
    if productsList is None:
        raise HTTPException(status_code=404, detail="No products found")
    return productsList

@router.get("/{product_id}", response_model=ProductResponse, dependencies=[Depends(verify_pm_role)])
async def read_product(product_id: str = Path(..., regex=r"^[a-fA-F0-9-]{36}$"), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    product = products.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(verify_pm_role)])
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    db_product = products.update_products(db, product_id, product)
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return db_product

@router.delete("/{product_id}", dependencies=[Depends(verify_pm_role)])
def delete_product(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_product = products.delete_products(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}

@router.put("/{product_id}/{quantity}", response_model=ProductResponse, dependencies=[Depends(verify_pm_role)])
def update_product_quantity(product_id: int, quantity: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    product = products.update_product_quantity(db, product_id, quantity)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/category/{category_id}", response_model=List[ProductResponse], dependencies=[Depends(verify_pm_role)])
def get_products_by_category(category_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    productsList = products.get_products_by_category_id(db, category_id)
    if not productsList:
        raise HTTPException(status_code=404, detail="No products found")
    return productsList
