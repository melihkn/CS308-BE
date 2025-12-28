import pytest
import sys
import os

# Proje kök dizinini PYTHONPATH'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from services.order_service import OrderService
from models.models import Order, Product, OrderItem
from datetime import datetime
from uuid import uuid4

@pytest.fixture
def mock_db_session():
    """
    Mock edilmiş bir SQLAlchemy veritabanı oturumu sağlar.
    """
    return Mock(spec=Session)

@pytest.fixture
def mock_product():
    """
    Mock bir ürün döner.
    """
    return Product(
        product_id="test-product-id",
        name="Test Product",
        price=50.0,
        quantity=10
    )

@pytest.fixture
def mock_order():
    """
    Mock bir sipariş döner.
    """
    return Order(
        order_id="test-order-id",
        customer_id="test-customer-id",
        total_price=100.0,
        order_date=datetime.now(),
        payment_status="paid",
        order_status=0
    )

def test_create_order(mock_db_session, mock_product):
    """
    Sipariş oluşturma işlemini test eder.
    """
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_product

    order_data = {
        "customer_id": "test-customer-id",
        "total_price": 100.0,
        "order_date": "2025-01-01",
        "payment_status": "paid",
        "invoice_link": None,
        "order_status": 0,
        "items": [
            {"product_id": "test-product-id", "quantity": 2, "price_at_purchase": 50.0}
        ]
    }

    with patch("services.InvoiceService.generate_invoice", return_value="invoice/path.pdf") as mock_invoice, \
         patch("services.EmailService.send_invoice_email") as mock_email:
        created_order = OrderService.create_order(order_data, mock_db_session)

        assert created_order.total_price == 100.0
        mock_invoice.assert_called_once()
        mock_email.assert_called_once()

def test_get_order(mock_db_session, mock_order):
    """
    Sipariş getirme işlemini test eder.
    """
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_order
    fetched_order = OrderService.get_order("test-order-id", mock_db_session)
    assert fetched_order.order_id == "test-order-id"

def test_update_order_status(mock_db_session, mock_order):
    """
    Sipariş durumunu güncelleme işlemini test eder.
    """
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_order
    updated_status = OrderService.update_order_status("test-order-id", 3, mock_db_session)
    assert updated_status == "delivered"

def test_process_payment(mock_db_session, mock_product):
    """
    Ödeme işlemini ve sipariş oluşturmayı test eder.
    """
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_product]

    payment_data = {
        "userId": "test-user-id",
        "deliveryAddress": "123 Test Street",
        "paymentDetails": {
            "cardNumber": "1234567890123456",
            "cvc": "123",
            "expiryMonth": "12",
            "expiryYear": "2025"
        },
        "cartItems": [
            {"product_id": "test-product-id", "quantity": 2}
        ]
    }

    with patch("services.InvoiceService.generate_invoice", return_value="invoice/path.pdf") as mock_invoice, \
         patch("services.EmailService.send_invoice_email") as mock_email:
        created_order = OrderService.process_payment(payment_data, mock_db_session)

        assert created_order.total_price == 100.0
        mock_invoice.assert_called_once()
        mock_email.assert_called_once()