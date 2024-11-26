from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dbContext import get_db
from services.categoryServices import create_category_, get_category, get_categories, update_category, delete_category
from schemas.categorySchemas import CategoryCreate, CategoryResponse
from dependencies import verify_pm_role, oauth2_scheme

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, dependencies=[Depends(verify_pm_role)])
async def add_category(category: CategoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return create_category_(db, category)

@router.get("/{category_id}", response_model=CategoryResponse, dependencies=[Depends(verify_pm_role)])
async def read_category(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/", response_model=list[CategoryResponse], dependencies=[Depends(verify_pm_role)])
async def read_all_categories(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_categories(db)

@router.delete("/{category_id}", dependencies=[Depends(verify_pm_role)])
async def remove_category(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_category = delete_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category