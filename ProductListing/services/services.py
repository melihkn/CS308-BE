from sqlalchemy.orm import Session
from ProductListing.models.models import ProductDB, ProductCreate, ProductUpdate, Review, ProductPopularity 
from typing import List, Optional
import uuid
from fastapi import Path
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import func, desc, asc, text
from fuzzywuzzy import fuzz


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> List[ProductDB]:
        return self.db.query(ProductDB).all()

    def get_product_by_id(self, product_id: str) -> Optional[ProductDB]:
        return self.db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

    def create_product(self, product_data: ProductCreate) -> ProductDB:
        
        product = ProductDB(**product_data.dict())
        try:
            new_product = ProductDB(**product.dict())
            self.db.add(new_product)
            self.db.commit()
            self.db.refresh(new_product)
            return new_product
        except Exception as e:
            raise ValueError(f"Error creating product: {e}")




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
    
    def get_products_sorted_by_popularity(self) -> List[ProductDB]:
        results = (
            self.db.query(ProductDB, ProductPopularity.popularity_score)
            .join(ProductPopularity, ProductPopularity.product_id == ProductDB.product_id)
            .order_by(ProductPopularity.popularity_score.desc())
            .all()
        )

        # Transform the result into a list of dicts compatible with Product schema
        popular_products = []
        for product, popularity_score in results:
            product_data = {
                "product_id": product.product_id,
                "name": product.name,
                "model": product.model,
                "description": product.description,
                "quantity": product.quantity,
                "item_sold": product.item_sold,
                "price": getattr(product, "price", 0),  # Ensure `price` exists
                "cost": getattr(product, "cost", 0),    # Ensure `cost` exists
                "warranty_status": product.warranty_status,
                "distributor": product.distributor,
                "image_url": product.image_url,
                "category_id": product.category_id,
            }
            popular_products.append(product_data)

        return popular_products
    
    def get_products_sorted_by_price(self, order: str = "asc") -> List[ProductDB]:
        """
        Get products sorted by price in ascending or descending order.
        
        :param order: "asc" for ascending, "desc" for descending
        :return: List of products sorted by price
        """
        if order == "desc":
            return self.db.query(ProductDB).order_by(desc(ProductDB.price)).all()
        return self.db.query(ProductDB).order_by(asc(ProductDB.price)).all()

    
    def update_popularity_scores(db: Session):
        # Calculate popularity score
        popularity_scores = (
            db.query(
                ProductDB.product_id,
                (func.sum(ProductDB.item_sold) * 0.5 +       # Weight for sales
                func.avg(Review.rating) * 0.3 +             # Weight for rating
                func.count(Review.review_id) * 0.2          # Weight for review count
                ).label("popularity_score")
            )
            .outerjoin(Review, Review.product_id == ProductDB.product_id)
            .group_by(ProductDB.product_id)
            .all()
        )

        # Update or insert popularity scores into `product_popularity`
        for product_id, score in popularity_scores:
            existing_entry = db.query(ProductPopularity).filter_by(product_id=product_id).first()
            if existing_entry:
                existing_entry.popularity_score = score
                existing_entry.last_updated = datetime.utcnow()
            else:
                new_entry = ProductPopularity(product_id=product_id, popularity_score=score, last_updated=datetime.utcnow())
                db.add(new_entry)

        db.commit()


    def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[ProductDB]:
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        # Convert product_data to a Pydantic model if it's a dictionary
        if isinstance(product_data, dict):
            product_data = ProductUpdate(**product_data)

        # Dynamically update fields provided in the request
        for key, value in product_data.model_dump(exclude_unset=True).items():
            if value is not None and hasattr(product, key):  # Check if the attribute exists
                setattr(product, key, value)  # Dynamically set attribute

        # Commit changes to the database
        self.db.commit()
        self.db.refresh(product)  # Refresh the product instance with updated values
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


    



    