import pytest
from sqlalchemy.orm import Session
from ..models.models import ShoppingCart, ShoppingCartItem, Product, Category



def test_add_item_to_cart(db_session: Session):
    # Test adding an item to the cart
    cart_item = db_session.query(ShoppingCartItem).first()
    assert cart_item is not None
    assert cart_item.quantity == 2

def test_remove_item_from_cart(db_session: Session):
    # Test removing an item from the cart
    cart_item = db_session.query(ShoppingCartItem).first()
    db_session.delete(cart_item)
    db_session.commit()

    cart_item = db_session.query(ShoppingCartItem).first()
    assert cart_item is None