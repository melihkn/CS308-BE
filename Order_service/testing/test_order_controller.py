import sys
import os

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # Eğer ana uygulama dosyanız 'main.py' ise
from fastapi.testclient import TestClient

# TestClient ile uygulama testleri için istemci oluştur
client = TestClient(app)

def test_health_check():
    """
    Health check endpoint'ini test eder.
    """
    response = client.get("/")  # Ana endpoint'e istek gönder
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Order Service!"}


def test_create_order():
    """
    Sipariş oluşturma endpoint'ini test eder.
    """
    order_data = {
        "order_id": "12345",
        "customer_id": "98765",
        "products": [
            {"product_id": "prod1", "quantity": 2},
            {"product_id": "prod2", "quantity": 1},
        ],
        "total_price": 150.75
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()["order_id"] == "12345"


def test_get_order():
    """
    Mevcut bir siparişi getirme endpoint'ini test eder.
    """
    order_id = "12345"
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["order_id"] == "12345"


def test_delete_order():
    """
    Sipariş silme endpoint'ini test eder.
    """
    order_id = "12345"
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}