import pytest
from fastapi.testclient import TestClient
from app import app  # FastAPI uygulamanızı buraya import edin
from unittest.mock import Mock

# Mock bir SQLAlchemy session fixture'ı
@pytest.fixture(scope="function")
def mock_db_session():
    """
    Mock bir veritabanı oturumu sağlar.
    """
    mock_session = Mock()
    yield mock_session

@pytest.fixture(scope="module")
def client():
    """
    FastAPI uygulamanıza HTTP istekleri yapmak için TestClient sağlar.
    """
    with TestClient(app) as test_client:
        yield test_client
