from sqlalchemy.orm import Session
from models.models import ProductDB, ProductCreate, ProductUpdate, ReviewDB, ProductPopularity, CategoryDB 
from typing import List, Optional
import uuid
from fastapi import Path
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import func, desc, asc, text
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import and_, or_
# Filter Parameters Model
class ProductFilterParams(BaseModel):
    sub_category: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    rating_min: Optional[float] = None
    warranty_status: Optional[int] = None


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_category_info_of_product(self,product_id: str) -> dict:
        """
        Fetches the category information for a specific product.

        Args:
            product_id (str): The ID of the product to fetch the category for.

        Returns:
            dict: The category information.

        Raises:
            ValueError: If the product or category is not found.
        """
        # Fetch the product from the database
        product = self.db.query(ProductDB).filter_by(product_id=product_id).first()
        if not product:
            raise ValueError("Product not found")

        # Ensure the product has a category ID
        if not product.category_id:
            raise ValueError("Product has no category assigned")

        # Fetch the category from the database
        category = self.db.query(CategoryDB).filter_by(category_id=product.category_id).first()
        if not category:
            raise ValueError("Category not found")

        # Return the category information as a dictionary
        return {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "parent_category_id": category.parentcategory_id
        }

     # ONLY 1 LEVEL DEPTH CATEGORIES ARE SUPPORTED

    # return the categories which have no parent category
    def get_root_categories(self) -> List[CategoryDB]:
        return self.db.query(CategoryDB).filter(CategoryDB.parentcategory_id == None).all()
    
    # return the categories which have the specified parent category
    def get_categories_by_parent_id(self, parent_id: str) -> List[CategoryDB]:
        return self.db.query(CategoryDB).filter(CategoryDB.parentcategory_id == parent_id).all()

    # root category girilirse subcategorilerindeki ürünler de dönülsün - detailed "/getproduct/category/{category_id}"
    def get_products_by_category_id(self, category_id: int) -> List[ProductDB]:
        # when items from root category is wanted, we return all the products in the subcategories of that root category
        
        # if the category is a root category
        if self.db.query(CategoryDB).filter(CategoryDB.category_id == category_id).first().parentcategory_id == None:
            # get all the subcategories of the root category
            subcategories = self.get_categories_by_parent_id(category_id)
            # get all the products in the subcategories
            products = []
            for subcategory in subcategories:
                products += self.db.query(ProductDB).filter(ProductDB.category_id == subcategory.category_id).all()
            return products
        # if the category is not a root category
        else:
            return self.db.query(ProductDB).filter(ProductDB.category_id == category_id).all()

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
                func.avg(ReviewDB.rating) * 0.3 +             # Weight for rating
                func.count(ReviewDB.review_id) * 0.2          # Weight for review count
                ).label("popularity_score")
            )
            .outerjoin(ReviewDB, ReviewDB.product_id == ProductDB.product_id)
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
    
    # TUNAHAN EKLENTİ - FILTERING

    """
    # Service to get products based on filters
    def filter_products(self, category_id: int, filter_params: ProductFilterParams) -> List[ProductDB]:
        # Start with all products in the specified category or its subcategories
        products = self.db.query(ProductDB)

        if filter_params.sub_category is None or filter_params.sub_category == 0:
            products = self.get_products_by_category_id(category_id)
        else:
            products = products.filter(ProductDB.category_id == filter_params.sub_category)


        # Apply price range filters
        if filter_params.price_min is not None:
            products = products.filter(ProductDB.price >= filter_params.price_min)
        if filter_params.price_max is not None:
            products = products.filter(ProductDB.price <= filter_params.price_max)

        # Apply rating filter
        if filter_params.rating_min is not None:
            products = products.outerjoin(ReviewDB, ProductDB.product_id == ReviewDB.product_id)\
                .group_by(ProductDB.product_id)\
                .having(func.avg(ReviewDB.rating) >= filter_params.rating_min)

        # Apply warranty filter
        if filter_params.warranty_status is not None:
            products = products.filter(ProductDB.warranty_status >= filter_params.warranty_status)

        # Execute the query and return results
        return products
    """
    def filter_products(self, category_id: int, filter_params: ProductFilterParams) -> List[ProductDB]:
        # Start with all products in the database
        products = self.db.query(ProductDB)

        # Check if a subcategory is specified, otherwise use root category and its subcategories
        if filter_params.sub_category is None or filter_params.sub_category == 0:
            # Fetch subcategories and include products from those
            subcategories = [category_id] + [
                sub.category_id for sub in self.get_categories_by_parent_id(category_id)
            ]
            products = products.filter(ProductDB.category_id.in_(subcategories))
        else:
            # Filter by the specified subcategory
            products = products.filter(ProductDB.category_id == filter_params.sub_category)

        # Apply price range filters
        if filter_params.price_min is not None:
            products = products.filter(ProductDB.price >= filter_params.price_min)
        if filter_params.price_max is not None:
            products = products.filter(ProductDB.price <= filter_params.price_max)

        # Apply rating filter
        if filter_params.rating_min is not None:
            products = products.outerjoin(ReviewDB, ProductDB.product_id == ReviewDB.product_id)\
                .group_by(ProductDB.product_id)\
                .having(func.avg(ReviewDB.rating) >= filter_params.rating_min)

        # Apply warranty filter
        if filter_params.warranty_status is not None:
            products = products.filter(ProductDB.warranty_status >= filter_params.warranty_status)

        # Execute the query and return results
        return products
