import pytest
from sqlalchemy.orm import Session
from ..models.models import Product, Category


def test_get_product_by_id(db_session: Session):
    # Test retrieving a product by ID
    product = db_session.query(Product).filter_by(product_id="00000000-0000-0000-0000-000000000002").first()
    assert product is not None
    assert product.name == "Test Product"

def test_update_product_quantity(db_session: Session):
    # Test updating product quantity
    product = db_session.query(Product).filter_by(product_id="00000000-0000-0000-0000-000000000002").first()
    product.quantity += 10
    db_session.commit()

    updated_product = db_session.query(Product).filter_by(product_id="00000000-0000-0000-0000-000000000002").first()
    assert updated_product.quantity == 110