from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dbContext import get_db
from models import WishlistItem
from schemas import WishlistItemCreate, WishlistItemResponse
from services.wishlist_item_service import WishlistItemService

router = APIRouter()
wishlist_item_service = WishlistItemService()

"""
Usage: to add an item to the wishlist we need to know the wishlist_id and product_id

example input to the create_wishlist_item endpoint:
{
    "wishlist_id": "1",
    "product_id": "1"
}

example output from the create_wishlist_item endpoint:
{
    "wishlist_item_id": "1", #this is learned after db.refresh() in the service layer and it is returned to the controller layer to return it to the user 
    "wishlist_id": "1",
    "product_id": "1"
}
"""
@router.post("/create", response_model=WishlistItemResponse) # response of this endpoint is WishlistItemResponse schema model object
def create_wishlist_item(wishlist_item: WishlistItemCreate, db: Session = Depends(get_db)):
    """Create a new wishlist item."""
    try:
        return wishlist_item_service.create_wishlist_item(wishlist_item, db)
    except ValueError as e: # if the wishlist is not found in the database or is not active, or product is not found in the database, or product is already in the wishlist
        # Map ValueError to HTTP 404 response
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle unexpected errors with 500 response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
"""
Usage:to get all wishlist items for a specific wishlist we need to know the wishlist_id

example query: /wishlist_items/get/1 (wishlist_id)

example output from the get_wishlist_items endpoint: (a list of WishlistItemResponse objects)
[
    {
        "wishlist_item_id": "1",
        "wishlist_id": "1",
        "product_id": "1"
    }
]
"""
@router.get("/get/{wishlist_id}", response_model=list[WishlistItemResponse]) # response of this endpoint is list of WishlistItemResponse schema model objects
def get_wishlist_items(wishlist_id: str, db: Session = Depends(get_db)):
    """Get all wishlist items for a specific wishlist."""
    try:
        return wishlist_item_service.get_wishlist_items(wishlist_id, db)
    except ValueError as e: # if the wishlist is not found in the database
        # Map ValueError to HTTP 404 response
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle unexpected errors with 500 response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

"""
usage: to remove an item from the wishlist we need to know the wishlist_item_id 

example query: /wishlist_items/delete/1 (wishlist_item_id)

example output from the delete_wishlist_item endpoint:
{
    "message": "Wishlist item deleted successfully"
}
"""
@router.delete("/delete/{wishlist_item_id}")
def delete_wishlist_item(wishlist_item_id: str, db: Session = Depends(get_db)):
    """Delete a wishlist item."""
    try:
        wishlist_item_service.delete_wishlist_item(wishlist_item_id, db)
    except ValueError as e: # if the wishlist item is not found in the database
        # Map ValueError to HTTP 404 response
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        # Handle unexpected errors with 500 response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    return {"message": "Wishlist item deleted successfully"} # if the deletion is successful we return this message to the user


"""
usage: to delete all wishlist items for a specific wishlist we need to know the wishlist_id

example query: /wishlist_items/delete_all/1 (wishlist_id)

example output from the delete_wishlist_items endpoint:
{
    "message": "All wishlist items deleted successfully"
}
"""
@router.delete("/delete_all/{wishlist_id}")
def delete_wishlist_items(wishlist_id: str, db: Session = Depends(get_db)):
    """Delete all wishlist items for a specific wishlist."""
    try:
        wishlist_item_service.delete_wishlist_items(wishlist_id, db)
    except ValueError as e: # if the wishlist is not found in the database
        # Map ValueError to HTTP 404 response
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        # Handle unexpected errors with 500 response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    return {"message": "All wishlist items deleted successfully"}

"""
usage: to get a specific wishlist item we need to know the wishlist_item_id

example query: /wishlist_items/get/1 (wishlist_item_id)

example output from the get_wishlist_item endpoint:
{
    "wishlist_item_id": "1",
    "wishlist_id": "wishlist_id",
    "product_id": "product_id"
}
"""
@router.get("/get_item/{wishlist_item_id}", response_model=WishlistItemResponse)
def get_wishlist_item(wishlist_item_id: str, db: Session = Depends(get_db)):
    """Get a specific wishlist item."""
    try:
        wishlist_item = wishlist_item_service.get_wishlist_item(wishlist_item_id, db)
        return wishlist_item
    except ValueError as e: # if the wishlist item is not found in the database
        # Map ValueError to HTTP 404 response
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        # Handle unexpected errors with 500 response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
# not: For error code, they are handled in controller. If there is an error in the service layer, it is raised as an exception (like ValueError, IndexError) and handled in the controller layer.



"""
usage: to update a wishlist item we need to know the wishlist_item_id and the new wishlist item data

example query: /wishlist_items/update/1 (wishlist_item_id)  
example input to the update_wishlist_item endpoint:
{
    "wishlist_id": "1",
    "product_id": "1"
}

example output from the update_wishlist_item endpoint:
{
    "wishlist_item_id": "1",
    "wishlist_id": "1",
    "product_id": "1"
}
"""
@router.put("/update/{wishlist_item_id}", response_model=WishlistItemResponse)
def update_wishlist_item(wishlist_item_id: str, wishlist_item: WishlistItemCreate, db: Session = Depends(get_db)):
    try: 
        return wishlist_item_service.update_wishlist_item(wishlist_item_id, wishlist_item, db)
    except ValueError as e: # if the wishlist item is not found in the database
        # Map ValueError to HTTP 404 response
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        # Handle unexpected errors with 500 response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    





