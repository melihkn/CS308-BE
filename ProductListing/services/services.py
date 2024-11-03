from sqlalchemy.orm import Session
from models.models import ProductDB, ProductCreate, ProductUpdate
from typing import List, Optional
import uuid

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> List[ProductDB]:
        return self.db.query(ProductDB).all()

    def get_product_by_id(self, product_id: str) -> Optional[ProductDB]:
    # No need for conversion since product_id is already a string
        return self.db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

        
    def create_product(self, product_data: ProductCreate) -> ProductDB:
        new_product = ProductDB(**product_data.dict())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def update_product(self, product_id: uuid.UUID, product_data: ProductUpdate) -> Optional[ProductDB]:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: uuid.UUID) -> bool:
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        return True
