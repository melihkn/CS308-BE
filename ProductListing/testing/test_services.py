from ProductListing.services import ProductService
from ProductListing.models.models import Review


def test_get_product_by_id(db_session):
    service = ProductService(db_session)
    product = service.get_product_by_id("00000000-0000-0000-0000-000000000002")
    assert product.name == "Dog Bed"


def test_update_product_service(db_session):
    service = ProductService(db_session)
    update_data = {
        "name": "Updated Dog Bed",
        "model": "DB-002",
        "description": "A comfortable dog bed",
        "quantity": 20,
        "price": 60.00,
        "cost": 50.00,
        "serial_number": "SN-UPDATED-DOG-BED-001",
        "item_sold": 5,
        "warranty_status": None,
        "distributor": "PetShopCo",
        "image_url": "https://images.com/dog-bed.jpg",
        "category_id": 1,
    }
    updated_product = service.update_product("00000000-0000-0000-0000-000000000002", update_data)
    assert updated_product.name == "Updated Dog Bed"
    assert updated_product.quantity == 20


def test_delete_product_service(db_session):
    service = ProductService(db_session)
    success = service.delete_product("00000000-0000-0000-0000-000000000002")
    assert success is True

def test_create_review_service(db_session):
    review = db_session.query(Review).first()
    assert review is not None
    assert review.pm_id == "00000000-0000-0000-0000-000000000003"
    assert review.approval_status == "Approved"

