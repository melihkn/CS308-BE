from sqlalchemy.orm import Session, joinedload
from models.models import Discount, Product, Wishlist, WishlistItem, Customer
from datetime import datetime
from services.EmailService import EmailService

def send_notification(customer_email: str, product_name: str, discount_rate: float):
    # For simplicity, we'll just log the notification
    # Replace this with actual email/SMS sending logic as needed

    print(f"Notification sent to {customer_email}: "
          f"The product '{product_name}' is now discounted by {discount_rate}%!")
    msg = f"The product '{product_name}' is now discounted by {discount_rate}%!"
    subj = "There is a DISCOUNTED Product in your wishlist!!"
    EmailService.send_discount_email(customer_email,subj,msg)

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

    # Step 2: Find the product and validate it exists
    product = db.query(Product).filter(Product.product_id == discount_data.product_id).first()
    if not product:
        raise ValueError("Product not found")

    # Step 3: Find customers who have this product in their wishlist
    # Explicitly join WishlistItem, Wishlist, and Customer to get customer information
    customers = (
        db.query(Customer.email)
        .join(Wishlist, Wishlist.customer_id == Customer.user_id)
        .join(WishlistItem, WishlistItem.wishlist_id == Wishlist.wishlist_id)
        .filter(WishlistItem.product_id == discount_data.product_id)
        .all()
    )

    # Step 4: Send notifications to each customer
    for customer_email, in customers:
        send_notification(customer_email, product.name, discount_data.discount_rate)

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

