from unittest.mock import Mock
from models.models import Customer
import pytest

# Mock bir SQLAlchemy session fixture'ı
@pytest.fixture(scope="function")
def mock_db_session():
    """
    Mock bir veritabanı oturumu sağlar.
    """
    mock_session = Mock()
    yield mock_session

def test_customer_creation(mock_db_session):
    # Yeni bir müşteri oluştur
    customer = Customer(
        name="John",
        surname="Doe",
        email="john.doe@example.com",
        password="hashedpassword123"
    )
    # Mock session üzerinde işlemler
    mock_db_session.add(customer)  # add çağrısı yapılır
    mock_db_session.commit()  # commit çağrısı yapılır

    # Mock nesnesi üzerinde doğrulamalar
    mock_db_session.add.assert_called_once_with(customer)  # add doğru şekilde çağrıldı mı?
    mock_db_session.commit.assert_called_once()  # commit doğru şekilde çağrıldı mı?

#DONE