from services.wishlist_item_service import WishlistItemService
from schemas import WishlistItemCreate
from models.models import Wishlist, WishlistItem, Product


def test_create_wishlist_item(db_session):
    service = WishlistItemService()
    data = WishlistItemCreate(
        wishlist_id="840416fd-99db-11ef-9ff5-80fa5b9b4ebf",
        product_id="84042531-99db-11ef-9ff5-80fa5b9b4ebg",
    )

    result = service.create_wishlist_item(data, db_session)

    assert result.wishlist_id == data.wishlist_id
    assert result.product_id == data.product_id
    assert db_session.query(WishlistItem).count() == 2  # Includes seeded data


def test_get_wishlist_items(db_session):
    service = WishlistItemService()

    result = service.get_wishlist_items("840416fd-99db-11ef-9ff5-80fa5b9b4ebf", db_session)

    assert len(result) > 0
    assert result[0].wishlist_id == "840416fd-99db-11ef-9ff5-80fa5b9b4ebf"


def test_delete_wishlist_item(db_session):
    service = WishlistItemService()

    service.delete_wishlist_item("84031531-99db-11ef-9ff5-80fa5b9b4ebf", db_session)

    assert db_session.query(WishlistItem).count() == 0  # Seeded item should be deleted


def test_delete_wishlist_items(db_session):
    service = WishlistItemService()

    service.delete_wishlist_items("840416fd-99db-11ef-9ff5-80fa5b9b4ebf", db_session)

    assert db_session.query(WishlistItem).count() == 0


def test_get_wishlist_item(db_session):
    service = WishlistItemService()

    result = service.get_wishlist_item("84031531-99db-11ef-9ff5-80fa5b9b4ebf", db_session)

    assert result.wishlist_item_id == "84031531-99db-11ef-9ff5-80fa5b9b4ebf"


def test_update_wishlist_item(db_session):
    service = WishlistItemService()
    data = WishlistItemCreate(
        wishlist_id="840416fd-99db-11ef-9ff5-80fa5b9b4ebf",
        product_id="84041531-99db-11ef-9ff5-80fa5b9b4ebf",
    )

    updated_item = service.update_wishlist_item(
        wishlist_item_id="84031531-99db-11ef-9ff5-80fa5b9b4ebf", wishlist_item=data, db=db_session
    )

    assert updated_item.wishlist_id == data.wishlist_id
    assert updated_item.product_id == data.product_id
