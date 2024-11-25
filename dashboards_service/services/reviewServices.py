from sqlalchemy.orm import Session
from models.models import Review
from schemas.reviewSchemas import ReviewCreate, ReviewApprovalUpdate
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
    return db.query(Review).all()