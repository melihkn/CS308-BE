from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_wishlist_item():
    data = {
        "wishlist_id": "840416fd-99db-11ef-9ff5-80fa5b9b4ebf",
        "product_id": "84041531-99db-11ef-9ff5-80fa5b9b4ebf",
    }

    response = client.post("/api/wishlist_items/create", json=data)

    assert response.status_code == 200
    assert response.json()["wishlist_id"] == data["wishlist_id"]
    assert response.json()["product_id"] == data["product_id"]


def test_get_wishlist_items():
    wishlist_id = "840416fd-99db-11ef-9ff5-80fa5b9b4ebf"

    response = client.get(f"/api/wishlist_items/get/{wishlist_id}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_wishlist_item():
    wishlist_item_id = "84031531-99db-11ef-9ff5-80fa5b9b4ebf"

    response = client.get(f"/api/wishlist_items/get_item/{wishlist_item_id}")

    assert response.status_code == 200
    assert response.json()["wishlist_item_id"] == wishlist_item_id


def test_update_wishlist_item():
    wishlist_item_id = "84031531-99db-11ef-9ff5-80fa5b9b4ebf"
    data = {
        "wishlist_id": "840416fd-99db-11ef-9ff5-80fa5b9b4ebf",
        "product_id": "84041531-99db-11ef-9ff5-80fa5b9b4ebf",
    }

    response = client.put(f"/api/wishlist_items/update/{wishlist_item_id}", json=data)

    assert response.status_code == 200
    assert response.json()["wishlist_item_id"] == wishlist_item_id
    assert response.json()["product_id"] == data["product_id"]


def test_delete_wishlist_item():
    wishlist_item_id = "84031531-99db-11ef-9ff5-80fa5b9b4ebf"

    response = client.delete(f"/api/wishlist_items/delete/{wishlist_item_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Wishlist item deleted successfully"
