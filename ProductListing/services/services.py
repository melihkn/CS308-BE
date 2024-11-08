from sqlalchemy.orm import Session
from models.models import ProductDB, ProductCreate, ProductUpdate 
from typing import List, Optional
import uuid
from fastapi import Path
from sqlalchemy.exc import IntegrityError




class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> List[ProductDB]:
        return self.db.query(ProductDB).all()

    def get_product_by_id(self, product_id: str) -> Optional[ProductDB]:
        return self.db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

    def create_product(self, product_data: ProductCreate) -> ProductDB:
        # Ensure product_id is not set manually; it will be auto-generated
        product_data_dict = product_data.dict()
        
        # Create a new ProductDB instance without product_id
        new_product = ProductDB(**product_data_dict)

        try:
            # Add and commit the new product
            self.db.add(new_product)
            self.db.commit()
            self.db.refresh(new_product)
            return new_product

        except IntegrityError as e:
            self.db.rollback()  # Roll back in case of error to prevent partial commit
            if "UNIQUE constraint failed" in str(e.orig):
                raise ValueError("A product with this serial number already exists.")
            raise ValueError("An error occurred while creating the product.") from e




    """
    def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[ProductDB]:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        

        # Only update fields that were explicitly provided in the request
        for key, value in product_data.items():

            product[key] = value
            

        self.db.commit()
        self.db.refresh(product)
        return product"""


    def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[ProductDB]:
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        # Only update fields that were explicitly provided in the request
        for key, value in product_data.dict(exclude_unset=True).items():
            if(value is not None):
                setattr(product, key, value)  # Dynamically set attribute

        # Commit changes to the database
        self.db.commit()
        self.db.refresh(product)
        return product



    def delete_product(self, product_id: str) -> bool:
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()  # No await here
        return True

    def search_product_by_name_description(self,query):

        results = self.db.query(ProductDB).filter(
        (ProductDB.name.ilike(f"%{query}%")) |  # Case-insensitive search for name
        (ProductDB.description.ilike(f"%{query}%"))  # Case-insensitive search for description
        ).all()
    
        # Convert results to a list of dictionaries to return as JSON
        return results