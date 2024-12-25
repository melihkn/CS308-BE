from services.wishlist_service import WishlistService
from schemas import WishlistCreate


def test_create_wishlist(db_session):
    service = WishlistService()
    data = WishlistCreate(name="Test Wishlist", customer_id="123", wishlist_status="active")
    
    result = service.create_wishlist(data, db_session)
    
    assert result.name == "Test Wishlist"
    assert result.customer_id == "123"
    assert result.wishlist_status == "active"

def test_get_wishlists_by_customer(db_session):
    service = WishlistService()
    data = WishlistCreate(name="Test Wishlist", customer_id="123", wishlist_status="active")
    service.create_wishlist(data, db_session)
    
    result = service.get_wishlists_by_customer("123", db_session)
    
    assert len(result) == 1
    assert result[0].name == "Test Wishlist"
