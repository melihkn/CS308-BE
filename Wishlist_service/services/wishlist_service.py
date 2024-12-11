from sqlalchemy.orm import Session
from models import Wishlist
from schemas import WishlistCreate

class WishlistService:
    def create_wishlist(self, wishlist_data: WishlistCreate, db: Session) -> Wishlist:
        """Create a new wishlist."""
        new_wishlist = Wishlist(
            name=wishlist_data.name,
            customer_id=wishlist_data.customer_id,
            wishlist_status=wishlist_data.wishlist_status,
        )
        db.add(new_wishlist)
        db.commit()
        db.refresh(new_wishlist)
        return new_wishlist

    def get_wishlists_by_customer(self, customer_id: str, db: Session) -> list[Wishlist]:
        """Retrieve all wishlists for a specific customer."""
        return db.query(Wishlist).filter(Wishlist.customer_id == customer_id).all()

    def update_wishlist(self, wishlist_id: str, wishlist_data: WishlistCreate, db: Session) -> Wishlist:
        """Update an existing wishlist."""
        wishlist = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id).first()
        if not wishlist:
            raise ValueError("Wishlist not found")
        wishlist.name = wishlist_data.name
        wishlist.wishlist_status = wishlist_data.wishlist_status
        db.commit()
        db.refresh(wishlist)
        return wishlist

    def delete_wishlist(self, wishlist_id: str, db: Session):
        """Delete a wishlist."""
        wishlist = db.query(Wishlist).filter(Wishlist.wishlist_id == wishlist_id).first()
        if not wishlist:
            raise ValueError("Wishlist not found")
        db.delete(wishlist)
        db.commit()
