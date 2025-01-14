import sys
import os

# Proje kök dizinini PYTHONPATH'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app  # FastAPI uygulaması
from controllers.refund_cancel_controller import router

# FastAPI uygulaması ile test istemcisini oluştur
app.include_router(router)
client = TestClient(app)

def test_refund_request_success():
    """
    Başarılı bir iade talebini test eder.
    """
    refund_data = {
        "order_id": "12345",
        "reason": "Product damaged",
        "amount": 150.75
    }
    response = client.post("/refund", json=refund_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Refund initiated successfully"}

def test_refund_request_invalid_data():
    """
    Geçersiz bir iade talebini test eder.
    """
    refund_data = {
        "order_id": "12345",
        # Eksik 'reason' alanı
        "amount": 150.75
    }
    response = client.post("/refund", json=refund_data)
    assert response.status_code == 422
    assert "reason" in response.json()["detail"]

def test_cancel_order_success():
    """
    Başarılı bir sipariş iptalini test eder.
    """
    order_id = "12345"
    response = client.delete(f"/cancel/{order_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Order canceled successfully"}

def test_cancel_order_not_found():
    """
    Olmayan bir siparişin iptalini test eder.
    """
    order_id = "99999"
    response = client.delete(f"/cancel/{order_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}