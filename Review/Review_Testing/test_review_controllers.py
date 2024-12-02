import pytest
from sqlalchemy.sql import text
from jose import jwt
from uuid import uuid4
from fastapi.testclient import TestClient
from ..app import app
from ..review_models.models import Review, Customer, Product,Order
from Authentication_service.utils.jwt_utils import create_access_token
from ..review_schemas.schemas import Review_Response, Get_Review_Response


client = TestClient(app)

def test_schema_check(db_session):
    result = db_session.execute(text("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'review'")).fetchall()
    assert len(result) > 0, "Review table does not exist."

def test_add_review(db_session):
    # Insert test customer, product, and order
    customer_id = str(uuid4())
    product_id = str(uuid4())
    order_id = str(uuid4())
    order_item_id = str(uuid4())
    unique_email = f"test_{uuid4().hex[:8]}@example.com"
    unique_serial = f"SN_{uuid4().hex[:8]}"

    # Insert customer
    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test", "surname": "User", "email": unique_email, "password": "hashedpassword"}
    )
    
    # Insert product
    db_session.execute(
        text("INSERT INTO products (product_id, name, model, price, cost, serial_number, quantity) VALUES "
             "(:product_id, :name, :model, :price, :cost, :serial_number, :quantity)"),
        {"product_id": product_id, "name": "Test Product", "model": "T123", "price": 99.99, "cost": 49.99, "serial_number": unique_serial, "quantity": 10}
    )
    
    # Insert order
    db_session.execute(
        text("INSERT INTO orders (order_id, customer_id, total_price, order_status, payment_status) VALUES "
             "(:order_id, :customer_id, :total_price, :order_status, :payment_status)"),
        {"order_id": order_id, "customer_id": customer_id, "total_price": 99.99, "order_status": 1, "payment_status": "paid"}
    )
    
    # Insert order item
    db_session.execute(
        text("INSERT INTO order_items (order_item_id, product_id, order_id, price_at_purchase, quantity) VALUES "
             "(:order_item_id, :product_id, :order_id, :price_at_purchase, :quantity)"),
        {
            "order_item_id": order_item_id,
            "product_id": product_id,
            "order_id": order_id,
            "price_at_purchase": 99.99,
            "quantity": 1
        }
    )
    db_session.commit()

    # Mock JWT token
    token = create_access_token(data={"sub": unique_email, "role": "customer"})
    
    # Create a payload for the review
    review_payload = {
        "product_id": product_id,
        "rating": 4,
        "comment": "Great product!"
    }

    # Make the request
    response = client.post(
        "/reviews/add_review",
        json=review_payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    # Assert the review was successfully added
    assert response.status_code == 200

    # Cleanup
    db_session.execute(text("DELETE FROM review WHERE product_id = :product_id"), {"product_id": product_id})
    db_session.execute(text("DELETE FROM order_items WHERE order_item_id = :order_item_id"), {"order_item_id": order_item_id})
    db_session.execute(text("DELETE FROM orders WHERE order_id = :order_id"), {"order_id": order_id})
    db_session.execute(text("DELETE FROM customers WHERE user_id = :user_id"), {"user_id": customer_id})
    db_session.execute(text("DELETE FROM products WHERE product_id = :product_id"), {"product_id":product_id}) 
    db_session.commit()


def test_get_reviews(db_session):
    # Insert test data
    customer_id = str(uuid4())
    product_id = str(uuid4())
    review_id = str(uuid4())
    unique_email = f"test_{uuid4().hex[:8]}@example.com"
    unique_serial = f"SN_{uuid4().hex[:8]}"

    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test User", "surname": "Doe", "email": unique_email, "password": "hashedpassword"}
    )
    db_session.execute(
        text("INSERT INTO products (product_id, name, model, price, cost, serial_number, quantity) VALUES "
             "(:product_id, :name, :model, :price, :cost, :serial_number, :quantity)"),
        {"product_id": product_id, "name": "Test Product", "model": "T123", "price": 99.99, "cost": 49.99, "serial_number": unique_serial, "quantity": 10}
    )
    db_session.execute(
        text("INSERT INTO review (review_id, customer_id, product_id, rating, comment, approval_status) VALUES "
             "(:review_id, :customer_id, :product_id, :rating, :comment, :approval_status)"),
        {"review_id": review_id, "customer_id": customer_id, "product_id": product_id, "rating": 5, "comment": "Excellent product", "approval_status": "approved"}
    )
    db_session.commit()

    # Test retrieving reviews
    response = client.get(f"/reviews/get_reviews/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    # Cleanup
    db_session.query(Review).filter_by(review_id=review_id).delete()
    db_session.query(Customer).filter_by(user_id=customer_id).delete()
    db_session.query(Product).filter_by(product_id=product_id).delete()
    db_session.commit()



def test_calculate_rating(db_session):
    # Insert test data
    customer_id = str(uuid4())
    product_id = str(uuid4())
    review_id = str(uuid4())
    unique_email = f"test_{uuid4().hex[:8]}@example.com"
    unique_serial = f"SN_{uuid4().hex[:8]}"

    # Insert customer
    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test User", "surname": "Doe", "email": unique_email, "password": "hashedpassword"}
    )

    # Insert product
    db_session.execute(
        text("INSERT INTO products (product_id, name, model, price, cost, serial_number, quantity) VALUES "
             "(:product_id, :name, :model, :price, :cost, :serial_number, :quantity)"),
        {"product_id": product_id, "name": "Test Product", "model": "T123", "price": 99.99, "cost": 49.99, "serial_number": unique_serial, "quantity": 10}
    )

    # Insert review
    db_session.execute(
        text("INSERT INTO review (review_id, customer_id, product_id, rating, comment, approval_status) VALUES "
             "(:review_id, :customer_id, :product_id, :rating, :comment, :approval_status)"),
        {"review_id": review_id, "customer_id": customer_id, "product_id": product_id, "rating": 4, "comment": "Good product", "approval_status": "APPROVED"}
    )
    db_session.commit()

    # Mock payload for Get_Review_Response


    # Make the request
    response = client.get(f"/reviews/calculate_rating/{product_id}")
    
    # Assertions
    assert response.status_code == 200
    print("auuu")
    print(response)
    data = response.json()
    print(data)
    assert data == 4.0

    # Cleanup
    db_session.query(Review).filter_by(review_id=review_id).delete()
    db_session.query(Customer).filter_by(user_id=customer_id).delete()
    db_session.query(Product).filter_by(product_id=product_id).delete()
    db_session.commit()

