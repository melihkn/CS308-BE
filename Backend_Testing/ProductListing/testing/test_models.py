import uuid
from ProductListing.models.models import ProductDB, Review

def test_product_model(db_session):
    product = db_session.query(ProductDB).filter_by(name="Dog Bed").first()
    assert product is not None
    assert product.name == "Dog Bed"


def test_review_model(db_session):
    review = db_session.query(Review).filter_by(rating=5).first()
    assert review is not None
    assert review.comment == "Excellent product!"

