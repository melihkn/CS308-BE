import pytest
from fastapi.testclient import TestClient
from ..main import app
from sqlalchemy.orm import Session
from ..models.models import ShoppingCart, ShoppingCartItem, Product, Category

client = TestClient(app)



def test_get_cart_items():
    response = client.get("/cart/cart-1")
    assert response.status_code == 200

def test_add_item_to_cart():
    response = client.post(
        "/cart/add",
        json={"product_id": "00000000-0000-0000-0000-000000000002", "quantity": 2, "customer_id": "84037c94-99db-11ef-9ff5-80fa5b9b4ebf"}
    )
    assert response.status_code == 200