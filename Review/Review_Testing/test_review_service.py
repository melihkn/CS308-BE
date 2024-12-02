import pytest
from sqlalchemy.sql import text
from uuid import uuid4
from ..review_services.review_service import create_review, get_all_reviews_for_certain_product, calculate_average_rating
from ..review_models.models import Review, Customer, Product
from ..review_schemas.schemas import Get_Review_Response, Review_Response
from uuid import uuid4
from sqlalchemy import text
from ..review_services.review_service import create_review  # Replace with your service import
from Authentication_service.utils.jwt_utils import SECRET_KEY,ALGORITHM,create_access_token

def test_create_review(setup_and_teardown):
    db_session = setup_and_teardown

    # Unique test data
    customer_id = str(uuid4())
    product_id = str(uuid4())
    unique_email = f"test_{uuid4().hex[:8]}@example.com"
    
    unique_serial = f"SN_{uuid4().hex[:8]}"

    # Insert test customer and product
    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test", "surname": "User", "email": unique_email, "password": "hashedpassword"}
    )
    db_session.execute(
        text("INSERT INTO products (product_id, name, model, price, cost, serial_number, quantity) VALUES "
             "(:product_id, :name, :model, :price, :cost, :serial_number, :quantity)"),
        {"product_id": product_id, "name": "Test Product", "model": "T123", "price": 99.99, "cost": 49.99, "serial_number": unique_serial, "quantity": 10}
    )
    db_session.commit()

    # Create a review
    
    access_token = create_access_token(data={"sub": unique_email, "role": "customer"})
    revie_response = Review_Response(product_id=product_id, rating=5,comment="Great product!")
    review = create_review(db_session, access_token,revie_response)

    # Assert the review was created
    assert review is not None
    review_id = review.review_id
    # Verify the review in the database
    result = db_session.execute(
        text("SELECT * FROM review WHERE review_id = :review_id"),
        {"review_id": review_id}
    ).fetchone()
 
    assert result is not None
    assert result[3] == 5
    assert result[4] == "Great product!"

def test_get_all_reviews_for_certain_product(db_session):
    # Insert test customer, product, and reviews
    customer_id = str(uuid4())
    product_id = str(uuid4())
    review_id1 = str(uuid4())
    review_id2 = str(uuid4())
    unique_email = f"test_{uuid4().hex[:8]}@example.com"
    
    unique_serial = f"SN_{uuid4().hex[:8]}"
    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test", "surname": "User", "email": unique_email, "password": "hashedpassword"}
    )
    db_session.execute(
        text("INSERT INTO products (product_id, name, model, price, cost, serial_number, quantity) VALUES "
             "(:product_id, :name, :model, :price, :cost, :serial_number, :quantity)"),
        {"product_id": product_id, "name": "Test Product", "model": "T123", "price": 99.99, "cost": 49.99, "serial_number": unique_serial, "quantity": 10}
    )
    db_session.execute(
        text("INSERT INTO review (review_id, customer_id, product_id, rating, comment, approval_status) VALUES "
             "(:review_id, :customer_id, :product_id, :rating, :comment, :approval_status)"),
        {"review_id": review_id1, "customer_id": customer_id, "product_id": product_id, "rating": 5, "comment": "Excellent product", "approval_status": "approved"}
    )
    db_session.execute(
        text("INSERT INTO review (review_id, customer_id, product_id, rating, comment, approval_status) VALUES "
             "(:review_id, :customer_id, :product_id, :rating, :comment, :approval_status)"),
        {"review_id": review_id2, "customer_id": customer_id, "product_id": product_id, "rating": 4, "comment": "Good product", "approval_status": "approved"}
    )
    db_session.commit()
    test_case = Get_Review_Response(product_id=product_id)
    # Fetch all reviews
    reviews = get_all_reviews_for_certain_product(db_session, test_case)
    assert len(reviews) == 2, "Failed to fetch all reviews for product."

    # Cleanup
    db_session.query(Review).filter(Review.product_id == product_id).delete()
    db_session.query(Customer).filter_by(user_id=customer_id).delete()
    db_session.query(Product).filter_by(product_id=product_id).delete()
    db_session.commit()


def test_calculate_average_rating(db_session):
    # Insert test customer, product, and reviews
    customer_id = str(uuid4())
    product_id = str(uuid4())
    review_id1 = str(uuid4())
    review_id2 = str(uuid4())
    unique_email = f"test_{uuid4().hex[:8]}@example.com"
    
    unique_serial = f"SN_{uuid4().hex[:8]}"
    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test", "surname": "User", "email": unique_email, "password": "hashedpassword"}
    )
    db_session.execute(
        text("INSERT INTO products (product_id, name, model, price, cost, serial_number, quantity) VALUES "
             "(:product_id, :name, :model, :price, :cost, :serial_number, :quantity)"),
        {"product_id": product_id, "name": "Test Product", "model": "T123", "price": 99.99, "cost": 49.99, "serial_number": unique_serial, "quantity": 10}
    )
    db_session.execute(
        text("INSERT INTO review (review_id, customer_id, product_id, rating, comment, approval_status) VALUES "
             "(:review_id, :customer_id, :product_id, :rating, :comment, :approval_status)"),
        {"review_id": review_id1, "customer_id": customer_id, "product_id": product_id, "rating": 5, "comment": "Excellent product", "approval_status": "approved"}
    )
    db_session.execute(
        text("INSERT INTO review (review_id, customer_id, product_id, rating, comment, approval_status) VALUES "
             "(:review_id, :customer_id, :product_id, :rating, :comment, :approval_status)"),
        {"review_id": review_id2, "customer_id": customer_id, "product_id": product_id, "rating": 3, "comment": "Okay product", "approval_status": "approved"}
    )
    db_session.commit()

    # Calculate average rating
    average_rating = calculate_average_rating(db_session, product_id)
    assert average_rating == 4, "Failed to calculate average rating."

    # Cleanup
    db_session.query(Review).filter(Review.product_id == product_id).delete()
    db_session.query(Customer).filter_by(user_id=customer_id).delete()
    db_session.query(Product).filter_by(product_id=product_id).delete()
    db_session.commit()
