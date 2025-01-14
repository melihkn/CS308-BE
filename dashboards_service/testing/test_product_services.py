import pytest
from unittest.mock import MagicMock
from decimal import Decimal
import sys
import os

# Proje kök dizinini PYTHONPATH'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.productServices import (
    create_product_service,
    update_product_service,
    delete_product_service,
    set_product_price,
)

@pytest.fixture
def mock_db():
    """
    Mock SQLAlchemy session.
    """
    return MagicMock()

def test_create_product_service(mock_db):
    product_data = MagicMock()
    product_data.dict.return_value = {"name": "Test Product", "price": Decimal("100.50"), "stock": 10}
    
    result = create_product_service(mock_db, product_data)
    mock_db.add.assert_called_once()  # Check if product is added to DB
    mock_db.commit.assert_called_once()  # Check if commit is called
    assert result.name == "Test Product"
    assert result.price == Decimal("100.50")
    assert result.stock == 10

def test_update_product_service(mock_db):
    product_data = MagicMock()
    product_data.dict.return_value = {"name": "Updated Product", "price": Decimal("150.75"), "stock": 5}
    
    mock_db.query.return_value.filter_by.return_value.first.return_value = MagicMock()
    result = update_product_service(mock_db, "12345", product_data)
    mock_db.commit.assert_called_once()  # Check if commit is called
    assert result.name == "Updated Product"
    assert result.price == Decimal("150.75")
    assert result.stock == 5

def test_delete_product_service(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = MagicMock()
    
    result = delete_product_service(mock_db, "12345")
    mock_db.delete.assert_called_once()  # Check if delete is called
    mock_db.commit.assert_called_once()  # Check if commit is called
    assert result == {"message": "product deleted successfully"}

def test_set_product_price(mock_db):
    mock_db.query.return_value.filter_by.return_value.first.return_value = MagicMock(price=Decimal("50.00"))
    
    result = set_product_price(mock_db, "12345", Decimal("75.25"))
    mock_db.commit.assert_called_once()  # Check if commit is called
    assert result.price == Decimal("75.25")