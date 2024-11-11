from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from dbContext import get_db
from services.reviewServices import create_review, get_reviews_by_status, update_review_status
from schemas.reviewSchemas import ReviewCreate, ReviewResponse, ReviewApprovalUpdate
from dependencies import verify_pm_role
from dependencies import oauth2_scheme
from dbContext import get_db
from jose import jwt
from settings import settings

router = APIRouter(prefix="/reviews", tags=["Reviews"])

#dependencies=Depends(verify_pm_role)
@router.post("/", response_model=ReviewResponse, dependencies=[Depends(verify_pm_role)])
async def submit_review(reviewCreate: ReviewCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    #payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #customer_id = payload.get("sub")
    review = create_review(db, reviewCreate, "2e742569-9d33-11ef-bff6-845cf33524ba")

    return review
#dependencies=Depends(verify_pm_role)
@router.get("/pending", response_model=List[ReviewResponse], dependencies=[Depends(verify_pm_role)])
async def get_pending_reviews(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    review = get_reviews_by_status(db, "pending")
    return review

#dependencies=Depends(verify_pm_role) , token: str = Depends(oauth2_scheme)
@router.patch("/{review_id}", dependencies=[Depends(verify_pm_role)])
async def update_review_status_(review_id : str, reviewApprovalUpdate: ReviewApprovalUpdate, db : Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    pm_id = payload.get("sub")
    print(pm_id)
    
    review_ = update_review_status(db, review_id, reviewApprovalUpdate)

    return {"approval_status": review_.approval_status}