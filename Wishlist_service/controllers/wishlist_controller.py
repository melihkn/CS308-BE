from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dbContext import get_db
from models import Wishlist
from schemas import WishlistCreate, WishlistResponse
from services.wishlist_service import WishlistService

router = APIRouter()
wishlist_service = WishlistService()

@router.post("/wishlists/", response_model=WishlistResponse)
def create_wishlist(wishlist_data: WishlistCreate, db: Session = Depends(get_db)):
    """Create a new wishlist."""
    try:
        return wishlist_service.create_wishlist(wishlist_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/wishlists/{customer_id}", response_model=list[WishlistResponse])
def get_wishlists(customer_id: str, db: Session = Depends(get_db)):
    """Get all wishlists for a customer."""
    return wishlist_service.get_wishlists_by_customer(customer_id, db)

@router.put("/wishlists/{wishlist_id}", response_model=WishlistResponse)
def update_wishlist(wishlist_id: str, wishlist_data: WishlistCreate, db: Session = Depends(get_db)):
    """Update a wishlist."""
    try:
        return wishlist_service.update_wishlist(wishlist_id, wishlist_data, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/wishlists/{wishlist_id}")
def delete_wishlist(wishlist_id: str, db: Session = Depends(get_db)):
    """Delete a wishlist."""
    try:
        wishlist_service.delete_wishlist(wishlist_id, db)
        return {"detail": "Wishlist deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
