from sqlalchemy.orm import Session
from models.models import Discount, Product, Wishlist, WishlistItem, Customer
from datetime import datetime

def send_notification(customer_email: str, product_name: str, discount_rate: float):
    # For simplicity, we'll just log the notification
    # Replace this with actual email/SMS sending logic as needed
    print(f"Notification sent to {customer_email}: "
          f"The product '{product_name}' is now discounted by {discount_rate}%!")

def get_discounts(db: Session):
    return db.query(Discount).all()

def create_discount_service(db: Session, discount_data):
     # Step 1: Apply the discount
    discount = Discount(
        product_id=discount_data.product_id,
        discount_rate=discount_data.discount_rate,
        start_date=discount_data.start_date,
        end_date=discount_data.end_date,
        is_active=True
    )
    db.add(discount)
    db.commit()
    db.refresh(discount)

    # Step 2: Find customers with the product in their wishlist
    product = db.query(Product).filter(Product.product_id == discount_data.product_id).first()
    if not product:
        raise ValueError("Product not found")

    # Query for customers with this product in their wishlist
    wishlist_items = db.query(WishlistItem).join(Wishlist).filter(
        WishlistItem.product_id == discount_data.product_id
    ).all()

    # Step 3: Notify each customer
    for item in wishlist_items:
        customer = db.query(Customer).filter(Customer.user_id == item.wishlist.customer_id).first()
        if customer and customer.email:
            send_notification(customer.email, product.name, discount_data.discount_rate)

    return discount
    

def update_discount_service(db: Session, discount_id: str, discount_data):
    discount = db.query(Discount).filter_by(discount_id=discount_id).first()
    if discount:
        for key, value in discount_data.dict().items():
            setattr(discount, key, value)
        db.commit()
        db.refresh(discount)
    return discount

def delete_discount_service(db: Session, discount_id: str):
    discount = db.query(Discount).filter_by(discount_id=discount_id).first()
    if discount:
        db.delete(discount)
        db.commit()
    return {"message": "Discount deleted successfully"}

