from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Import the CartService class from the services.cart_service module
from services.cart_service import CartService
from utils.db_utils import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter()

# pdyanctic model for the cart item which is to be used when adding an item to the cart with certain quantity
class CartItem(BaseModel):
    product_id: str
    quantity: int

@router.post("/cart/add")
async def add_to_cart(cart_item: CartItem, customer_id: str = None, db: Session = Depends(get_db)):
    """
    Add an item to the user's shopping cart.
    - If `customer_id` is provided, store the item in the persistent cart in the database.
    - If `customer_id` is not provided, the frontend will handle session-based storage.
    """
    if customer_id:
        try:
            CartService.add_item_to_persistent_cart(cart_item, customer_id, db)
            return {"message": "Item added to persistent cart.", "cart_items": CartService.get_cart(customer_id, db)}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Could not add item to cart.")
    else:
        return {"message": "Item added to session-based cart (handled on frontend)."}

@router.post("/cart/merge")
async def merge_cart(items: List[CartItem], customer_id: str, db: Session = Depends(get_db)):
    """
    Merge a session-based cart with the persistent cart after user login.
    """
    return CartService.merge_session_cart_with_persistent_cart(items, customer_id, db)

@router.delete("/cart/remove")
async def remove_from_cart(product_id: str, customer_id: str, db: Session = Depends(get_db)):
    """
    Remove an item from the user's persistent cart in the database.
    """
    return CartService.remove_item_from_cart(product_id, customer_id, db)


@router.get("/cart/{customer_id}")
async def get_cart(customer_id: str, db: Session = Depends(get_db)):
    """
    Get the user's shopping cart.
    """
    return CartService.get_cart(customer_id, db)

@router.delete("/cart/clear/{customer_id}")
async def clear_cart(customer_id: str, db: Session = Depends(get_db)):
    """
    Clear the user's shopping cart.
    """
    return CartService.clear_cart(customer_id, db)

@router.patch("/cart/decrease_quantity")
async def decrease_item_quantity(product_id: str, customer_id: str, db: Session = Depends(get_db)):
    """
    Decrease the quantity of an item by 1 in the cart.
    - If the quantity is already 1, remove the item.

    params:
    - product_id: str
    - customer_id: str
    - db: Session

    returns:
    - a message indicating the success of the operation coming from the CartService.decrease_item_quantity method
    """
    try:
        result = CartService.decrease_item_quantity(product_id, customer_id, db)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not decrease item quantity in the cart.")

@router.patch("/cart/increase_quantity")
async def increase_item_quantity(product_id: str, customer_id: str, db: Session = Depends(get_db)):
    """
    Increase the quantity of an item by 1 in the cart.

    params:
    - product_id: str
    - customer_id: str
    - db: Session

    returns:
    - a message indicating the success of the operation coming from the CartService.increase_item_quantity method
    """
    try:
        result = CartService.increase_item_quantity(product_id, customer_id, db)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not increase item quantity in the cart.")

