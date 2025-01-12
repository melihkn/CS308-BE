from sqlalchemy.orm import Session
from models.models import Product, Discount
from fastapi import HTTPException
from sqlalchemy import and_



# This service is for in shopping card FE, to get the product details, update the quantity of the product, get all products, increment the number of items sold for a product, and check if a product is in stock.
class ProductService:
    @staticmethod
    def get_product_by_id(product_id: str, db: Session):
        """
        Retrieve product information by product ID.
        
        Parameters:
        - product_id (str): The ID of the product to retrieve.
        - db (Session): The database session.
        
        Returns:
        - dict: A dictionary with product details or raises an HTTP 404 if the product is not found.
        """
        product = db.query(Product).filter(Product.product_id == product_id).first()
        discount = db.query(Discount).filter(and_(Discount.product_id == product.product_id, Discount.is_active)).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if discount:
            return {
            "product_id": product.product_id,
            "name": product.name,
            "model": product.model,
            "description": product.description,
            "quantity": product.quantity,
            "price": float(product.price),
            "distributor": product.distributor,
            "image_url": product.image_url,
            "discount_rate": float(discount.discount_rate)
        }
        else:
            return {
            "product_id": product.product_id,
            "name": product.name,
            "model": product.model,
            "description": product.description,
            "quantity": product.quantity,
            "price": float(product.price),
            "distributor": product.distributor,
            "image_url": product.image_url,
            "discount": 0
        }

        

    @staticmethod
    def update_product_quantity(product_id: str, quantity: int, db: Session):
        """
        Update the quantity of a product by product ID.
        
        Parameters:
        - product_id (str): The ID of the product.
        - quantity (int): The new quantity to set for the product.
        - db (Session): The database session.
        
        Returns:
        - dict: A message indicating success or failure.
        """
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if quantity < 0:
            raise HTTPException(status_code=400, detail="Quantity cannot be negative")
        
        product.quantity = quantity
        db.commit()
        return {"message": f"Quantity for product {product_id} updated to {quantity}"}

    @staticmethod
    def get_all_products(db: Session):
        """
        Retrieve all products to display on the homepage or main product listing.
        
        Parameters:
        - db (Session): The database session.
        
        Returns:
        - list: A list of dictionaries, each representing a product.
        """
        products = db.query(Product).all()
        return [
            {
                "product_id": product.product_id,
                "name": product.name,
                "model": product.model,
                "description": product.description,
                "quantity": product.quantity,
                "price": float(product.price),
                "distributor": product.distributor,
                "image_url": product.image_url,
            }
            for product in products
        ]

    @staticmethod
    def increment_item_sold(product_id: str, quantity_sold: int, db: Session):
        """
        Increment the number of items sold for a product.
        
        Parameters:
        - product_id (str): The ID of the product.
        - quantity_sold (int): The quantity to increment by.
        - db (Session): The database session.
        
        Returns:
        - dict: A message indicating success or failure.
        """
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.item_sold += quantity_sold
        db.commit()
        return {"message": f"Sold quantity updated for product {product_id}"}

    @staticmethod
    def get_product_inventory_status(product_id: str, db: Session):
        """
        Check if a product is in stock and return relevant info.
        
        Parameters:
        - product_id (str): The ID of the product to check.
        - db (Session): The database session.
        
        Returns:
        - dict: Product inventory status.
        """
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "product_id": product.product_id,
            "name": product.name,
            "quantity": product.quantity,
            "in_stock": product.quantity > 0,
        }
