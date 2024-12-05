import pytest
from fastapi.testclient import TestClient
from ..main import app
from sqlalchemy.orm import Session
from ..models.models import Product, Category

client = TestClient(app)


def test_get_all_products():
    response = client.get("/products")
    assert response.status_code == 200