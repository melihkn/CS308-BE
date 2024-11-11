# app/schemas/category.py

from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    category_name: str
    parentcategory_id: Optional[int] = None

class CategoryResponse(CategoryCreate):
    category_id: int
