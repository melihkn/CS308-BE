from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from ..review_dependencies import oauth2_scheme, verify_user_role
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ..review_settings import settings
from ..dbContext_Review import get_db
from ..review_models.models import Customer, Review,Order,OrderItem
from uuid import uuid4
from sqlalchemy import and_
from ..review_schemas.schemas import Review_Response,Get_Review_Response,Review_Request

def check_user_orders(db: Session, token: str ,product_id: str):
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    email : str = payload.get("sub")
    user = db.query(Customer).filter(Customer.email == email).first()
    user_id = user.user_id
    result = (db.query(OrderItem).join(Order, OrderItem.order_id == Order.order_id).filter(and_(Order.customer_id == user_id,OrderItem.product_id == product_id )).first())
    if result:
        return True
    else:
        return False


def create_review(db: Session, token: str, submitted_review: Review_Request):
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    email : str = payload.get("sub")
    user = db.query(Customer).filter(Customer.email == email).first()
    user_id = user.user_id
    approval_status = "APPROVED" if submitted_review.comment == "" else "PENDING"
    review = Review(
        review_id = str(uuid4()),
        customer_id = user_id,
        product_id = submitted_review.product_id,
        rating = submitted_review.rating,
        comment = submitted_review.comment,
        approval_status = approval_status
    )

    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_all_reviews_for_certain_product(db: Session, requested_review: Get_Review_Response):
    """
    Fetch all reviews for a specific product.

    Args:
        db (Session): Database session.
        product_id (str): The ID of the product.

    Returns:
        List[Review]: A list of reviews for the product.
    """
    reviews = (
        db.query(Review)
        .filter(
            Review.product_id == requested_review.product_id,
            Review.approval_status == "APPROVED"
        )
        .all()
    )
    return reviews


def calculate_average_rating(db: Session, product_id: str):
    reviews = db.query(Review).filter(Review.product_id == product_id,
                                      Review.approval_status == "APPROVED"
                                      ).all()
    
    if len(reviews) == 0:
        return 0
    else:
        avg = 0
        for i in reviews:
            avg += i.rating
        avg = avg/len(reviews)
        return avg