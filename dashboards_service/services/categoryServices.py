from sqlalchemy.orm import Session
from models.models import Category
from schemas.categorySchemas import CategoryCreate

def create_category_(db: Session, category: CategoryCreate):
    category = Category(category_name=category.category_name, parentcategory_id=category.parentcategory_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.query(Category).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()

def update_category_(db: Session, category_id: int, category: CategoryCreate):
    category_ = db.query(Category).filter(Category.category_id == category_id).first()

    for key, value in category.dict().items():
        if value is not None:
            setattr(category_, key, value)
    
    db.commit()
    db.refresh(category_)
    return category_

def delete_category(db: Session, category_id : int):
    category_ = db.query(Category).filter(Category.category_id == category_id).first()

    if not category_:
        return None
    
    db.delete(category_)
    db.commit()

    return {"message" : "Category deleted succesfully!"}