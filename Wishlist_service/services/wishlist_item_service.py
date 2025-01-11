from sqlalchemy.orm import Session
from models import Wishlist, WishlistItem, Product
from schemas import WishlistItemCreate

class WishlistItemService:
    
    def create_wishlist_item(self, wishlist_item: WishlistItemCreate, db: Session) -> WishlistItem:
        """
        This service is to add an item to the wishlist.

        Args:
        wishlist_item : WishlistItemCreate : Pydantic model for WishlistItemCreate
        db : Session : SQLAlchemy Session

        Returns:
        WishlistItem : SQLAlchemy model for WishlistItem
        """
        # Find the wishlist to add the item (only active ones can be used to add items)
        wishlist = db.query(Wishlist).filter(
            Wishlist.wishlist_id == wishlist_item.wishlist_id,  # Use the Pydantic object directly
            Wishlist.wishlist_status == "active"
        ).first()

        if not wishlist:
            raise ValueError("Wishlist not found or is not active")

        # Find the product to add to the wishlist
        product = db.query(Product).filter(
            Product.product_id == wishlist_item.product_id
        ).first()

        if not product:
            raise ValueError("Product not found in the database")

        # check whether the product is already in the wishlist
        wishlist_item_exists = db.query(WishlistItem).filter(
            WishlistItem.wishlist_id == wishlist_item.wishlist_id,
            WishlistItem.product_id == wishlist_item.product_id
        ).first()

        if wishlist_item_exists:
            raise ValueError("Product already exists in the wishlist")

        # Create a new wishlist item object if the product is not in the wishlist
        new_wishlist_item = WishlistItem(
            wishlist_id=wishlist_item.wishlist_id,
            product_id=wishlist_item.product_id
        )

        db.add(new_wishlist_item)  # Add the new wishlist item to the database
        db.commit()
        db.refresh(new_wishlist_item)  # Refresh to get the new ID from the database
        return new_wishlist_item # we return the new wishlist item object (sql alchemy object) to the controller to return it to the user 
    

    def get_wishlist_items(self, wishlist_id: str, db: Session) -> list[WishlistItem]:
        """
        This service is to get all wishlist items for a specific wishlist.

        Args:
        wishlist_id : str : UUID of the wishlist
        db : Session : SQLAlchemy Session

        Returns:
        list[WishlistItem] : List of SQLAlchemy model for WishlistItem
        """
        # Check whether the wishlist exists
        wishlist = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id).first()
        if not wishlist:
            raise ValueError("Wishlist not found in the database")
        
        WishlistItemsOfWishList = []
        for item in wishlist.wishlist_items:
            WishlistItemsOfWishList.append(item)

        # Get all wishlist items for the given wishlist
        return WishlistItemsOfWishList #no need for that again: db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).all()
    

    def delete_wishlist_item(self, wishlist_item_id: str, db: Session):
        """
        This service is to delete a wishlist item.

        Args:
        wishlist_item_id : str : UUID of the wishlist item
        db : Session : SQLAlchemy Session
        """
        # Find the wishlist item to delete
        wishlist_item = db.query(WishlistItem).filter(WishlistItem.wishlist_item_id == wishlist_item_id).first()
        if not wishlist_item:
            raise ValueError("Wishlist item not found in the database")
        db.delete(wishlist_item)
        db.commit()
        return {"message": "Wishlist item deleted successfully"}
    
    def delete_wishlist_items(self, wishlist_id: str, db: Session):
        """
        This service is to delete all wishlist items for a specific wishlist.

        Args:   
        wishlist_id : str : UUID of the wishlist
        db : Session : SQLAlchemy Session
        """
        # Check whether the wishlist exists
        wishlist = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id).first()
        if not wishlist:
            raise ValueError("Wishlist not found in the database")

        # Get all wishlist items for the given wishlist
        wishlist_items = db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).all()
        for item in wishlist_items:
            db.delete(item)
        db.commit()
        return {"message": "All wishlist items deleted successfully for the wishlist"}
    
    def get_wishlist_item(self, wishlist_item_id: str, db: Session) -> WishlistItem:
        """
        This service is to get a specific wishlist item.

        Args:
        wishlist_item_id : str : UUID of the wishlist item
        db : Session : SQLAlchemy Session
        
        Returns:
        WishlistItem : SQLAlchemy model for WishlistItem
        """

        # Find the wishlist item to return
        wishlist_item = db.query(WishlistItem).filter(WishlistItem.wishlist_item_id == wishlist_item_id).first()
        if not wishlist_item:
            raise ValueError("Wishlist item not found in the database")
        return wishlist_item
    
    def update_wishlist_item(self, wishlist_item_id: str, wishlist_item: WishlistItemCreate, db: Session) -> WishlistItem:
        """
        This service is to update a wishlist item.

        Args:   
        wishlist_item_id : str : UUID of the wishlist item
        wishlist_item : WishlistItemCreate : Pydantic model for WishlistItemCreate
        db : Session : SQLAlchemy Session
        """

        # Find the wishlist item to update
        wishlist_item = db.query(WishlistItem).filter(WishlistItem.wishlist_item_id == wishlist_item_id).first()
        if not wishlist_item:
            raise ValueError("Wishlist item not found in the database")
        
        # Update the wishlist item
        wishlist_item.wishlist_id = wishlist_item.wishlist_id
        wishlist_item.product_id = wishlist_item.product_id
        db.commit()
        db.refresh(wishlist_item)
        return wishlist_item


