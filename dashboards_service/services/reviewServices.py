from typing import List
from sqlalchemy.orm import Session
from models.models import Customer, Product, Review
from schemas.reviewSchemas import ReviewCreate, ReviewApprovalUpdate, ReviewResponse
from uuid import uuid4

def create_review(db: Session, reviewCreate: ReviewCreate, customer_id: str):
    review = Review(
        review_id = str(uuid4()),  
        product_id = reviewCreate.product_id,
        rating = reviewCreate.rating,
        comment = reviewCreate.comment,
        approval_status = "PENDING"
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_status(db: Session, status: str):
    return db.query(Review).filter(Review.approval_status == status).all()

def update_review_status(db: Session, review_id: str, reviewApprovalUpdate: ReviewApprovalUpdate, pm_id : str = None):
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if review is None:
        return None
    review.approval_status = reviewApprovalUpdate.approval_status
    if pm_id:
        review.pm_id = pm_id
    db.commit()
    db.refresh(review)
    return review

def get_reviews_(db : Session):
    reviews = db.query(Review).all()

    reviews_ = []

    for review in reviews:
        product = db.query(Product).filter(Product.product_id == review.product_id).first()
        user = db.query(Customer).filter(Customer.user_id == review.customer_id).first()
        if user.middlename is None:
            name = user.name + " " + user.surname
        else:
            name = user.name + " " + user.middlename + " " + user.surname
        reviews_.append(ReviewResponse(
            review_id = review.review_id,
            image_url = product.image_url,
            customer_id = review.customer_id,
            customer_name = name,
            product_name = product.name,
            product_id = review.product_id,
            rating = review.rating,
            comment = review.comment,
            approval_status = review.approval_status
        ))
    return reviews_

def delete_review(db: Session, review_id: str, pm_id: str):
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if review is None:
        return None
    db.delete(review)
    db.commit()
    return review