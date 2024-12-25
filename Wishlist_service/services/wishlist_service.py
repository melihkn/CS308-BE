from sqlalchemy.orm import Session
from models.models import Wishlist
from schemas import WishlistCreate

class WishlistService:
    def create_wishlist(self, wishlist_data: WishlistCreate, db: Session) -> Wishlist:
        """Create a new wishlist."""
        # lets check whether there is a wishlist with the same name and active status   
        wishlist = db.query(Wishlist).filter(Wishlist.name == wishlist_data.name, Wishlist.wishlist_status == "active").first()
        if wishlist:
            raise ValueError("Wishlist with the same name already exists")

        # if not exists create a new wishlist
        new_wishlist = Wishlist(
            name=wishlist_data.name,
            customer_id=wishlist_data.customer_id,
            wishlist_status=wishlist_data.wishlist_status,
        )
        db.add(new_wishlist) # add the new wishlist to the database
        db.commit() # commit the transaction 
        db.refresh(new_wishlist) # refresh the new_wishlist object to get the new id from the database 
        return new_wishlist # return the new wishlist object 

    def get_wishlists_by_customer(self, customer_id: str, db: Session) -> list[Wishlist]:
        """Retrieve all active wishlists for a specific customer."""
        # if no customer found , raise Value error
        customer = db.query(Wishlist).filter(Wishlist.customer_id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")

        # get all active wishlists for a specific customer
        wishlists = db.query(Wishlist).filter(Wishlist.customer_id == customer_id, Wishlist.wishlist_status == "active").all()
        return wishlists # return the list of wishlists to the controller


    def update_wishlist(self, wishlist_id: str, wishlist_data: WishlistCreate, db: Session) -> Wishlist:
        """Update an existing and active wishlist."""
        # Check whether the wishlist exists and its status is active 
        wishlist = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id, Wishlist.wishlist_status == "active").first()
        if not wishlist:
            raise ValueError("Wishlist not found or is not active")
        wishlist.name = wishlist_data.name
        wishlist.wishlist_status = wishlist_data.wishlist_status
        db.commit()
        db.refresh(wishlist)
        return wishlist # return the sql alchemy object of the updated wishlist to the controller 

    def delete_wishlist(self, wishlist_id: str, db: Session):
        """Delete a wishlist."""
        wishlist = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id, Wishlist.wishlist_status == "active").first()
        if not wishlist:
            raise ValueError("Wishlist not found or is not active")
        db.delete(wishlist) # delete the wishlist from the database
        db.commit() # commit the transaction
        return {"message": "Wishlist deleted successfully"}
