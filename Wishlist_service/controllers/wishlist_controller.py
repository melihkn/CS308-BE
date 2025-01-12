from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dbContext import get_db
from models import Wishlist
from schemas import WishlistCreate, WishlistResponse
from services.wishlist_service import WishlistService

router = APIRouter()
wishlist_service = WishlistService()


"""
example input to the create_wishlist endpoint:
{
    "name": "My Wishlist",
    "customer_id": "1",
    "wishlist_status": "active"
}

example output from the create_wishlist endpoint:
{
    "wishlist_id": "1",
    "name": "My Wishlist",
    "customer_id": "1",
    "wishlist_status": "active"
}
"""
@router.post("/create", response_model=WishlistResponse)
def create_wishlist(wishlist_data: WishlistCreate, db: Session = Depends(get_db)):
    """Create a new wishlist."""
    try:
        return wishlist_service.create_wishlist(wishlist_data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # wishlist with the same name already exists, an expected error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") # unexpected error


"""
get_wishlists endpoint is used to get all wishlists for a customer.

It's an get request that takes a customer_id as a parameter.
example query: /wishlists/customer/1 (customer_id)


example output from the get_wishlists endpoint:
[
    {
        "wishlist_id": "1",
        "name": "My Wishlist",
        "customer_id": "1",
        "wishlist_status": "active"
    }
]
"""
@router.get("/get/{customer_id}", response_model=list[WishlistResponse])
def get_wishlists(customer_id: str, db: Session = Depends(get_db)):
    """Get all wishlists for a customer."""
    """After some modificitations customer id is sent as a tokent itself, then token is decoded in wishlist service"""
    try:
        WishLists = wishlist_service.get_wishlists_by_customer(customer_id, db)
        return WishLists
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # customer not found, an expected error 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") # for unexpected errors

"""
update_wishlist endpoint is used to update a wishlist.

It's an put request that takes a wishlist_id as a parameter and a WishlistCreate object as a body.
example query: /wishlists/wishlist/1 (wishlist id)

example input to the update_wishlist endpoint:
"""
@router.put("/update/{wishlist_id}", response_model=WishlistResponse)
def update_wishlist(wishlist_id: str, wishlist_data: WishlistCreate, db: Session = Depends(get_db)):
    """Update a wishlist."""
    try:
        return wishlist_service.update_wishlist(wishlist_id, wishlist_data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # if the wishlist is not found in the database or is not active, an expected error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") # any other unexpected errors

# to delete a wishlist
@router.delete("/delete/{wishlist_id}")
def delete_wishlist(wishlist_id: str, db: Session = Depends(get_db)):
    """Delete a wishlist."""
    try:
        return wishlist_service.delete_wishlist(wishlist_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # if the wishlist is not found in the database or is not active, an expected error 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") # any other unexpected errors
