from fastapi.testclient import TestClient
from main import app
from models.models import Customer, Wishlist, Product, WishlistItem

client = TestClient(app)




def test_create_wishlist():
    data = {
        "name": "New Wishlist",
        "customer_id": "84037c94-99db-11ef-9ff5-80fa5b9b4ebf",
        "wishlist_status": "active"
    }

    # Add the correct prefix
    response = client.post("/api/wishlists/create", json=data)

    assert response.status_code == 200
    assert response.json()["name"] == "New Wishlist"
    assert response.json()["customer_id"] == "84037c94-99db-11ef-9ff5-80fa5b9b4ebf"
    assert response.json()["wishlist_status"] == "active"


def test_get_wishlists():
    customer_id = "84037c94-99db-11ef-9ff5-80fa5b9b4ebf"

    # Add the correct prefix
    response = client.get(f"/api/wishlists/get/{customer_id}")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_wishlist():
    data = {
        "name": "Updated Wishlist",
        "customer_id": "84037c94-99db-11ef-9ff5-80fa5b9b4ebf",
        "wishlist_status": "active"
    }
    wishlist_id = "840416fd-99db-11ef-9ff5-80fa5b9b4ebf"

    # Add the correct prefix
    response = client.put(f"/api/wishlists/update/{wishlist_id}", json=data)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Wishlist"
    assert response.json()["wishlist_status"] == "active"


def test_delete_wishlist():
    wishlist_id = "840416fd-99db-11ef-9ff5-80fa5b9b4ebf"

    # Add the correct prefix
    response = client.delete(f"/api/wishlists/delete/{wishlist_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Wishlist deleted successfully"
