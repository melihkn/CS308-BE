from Authentication_service.utils.jwt_utils import SECRET_KEY,ALGORITHM,create_access_token
from ..review_settings import settings  # Replace with your actual settings
from uuid import uuid4
from sqlalchemy.sql import text
from ..review_dependencies import verify_user_role
from fastapi import HTTPException
import pytest
def test_verify_user_role_success(setup_and_teardown):
    db_session = setup_and_teardown

    # Generate a valid JWT token
    test_email = f"test_{uuid4().hex[:8]}@example.com"
    
    # Insert test customer
    customer_id = str(uuid4())
    db_session.execute(
        text("INSERT INTO customers (user_id, name, surname, email, password) VALUES (:user_id, :name, :surname, :email, :password)"),
        {"user_id": customer_id, "name": "Test", "surname": "User", "email": test_email, "password": "hashedpassword"}
    )
    db_session.commit()
    
    token = create_access_token(data={"sub": test_email, "role": "customer"})
    
    # Verify no exception is raised
    try:
        verify_user_role(token=token, db=db_session)
        db_session.rollback()
    except HTTPException as e:
        pytest.fail(f"verify_user_role raised an exception: {e}")
        db_session.rollback()
