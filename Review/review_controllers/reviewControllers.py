from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from review_services import review_service
from review_dependencies import oauth2_scheme, verify_user_role
from typing import Optional
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from review_settings import settings
from dbContext_Review import get_db
from review_models.models import Customer

from review_services.review_service import check_user_orders, create_review,get_all_reviews_for_certain_product,calculate_average_rating


router = APIRouter(prefix="/reviews")



class Review_Response(BaseModel):
    product_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

@router.post("/add_review",response_model=Review_Response,dependencies=[Depends(verify_user_role)])
async def add_review(submited_review: Review_Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    #checks if the user of the token ordered the product whose id's is given as parameter
    check = check_user_orders(db, token, submited_review.product_id)
    if(check):
        return create_review(db,token,submited_review)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not ordered that product, so you cannot review it"
        )
    
@router.get("/get_reviews", response_model = List[Review_Response])
async def get_reviews(requested_reviews: Review_Response,db: Session = Depends(get_db)):
    reviews = get_all_reviews_for_certain_product(db,requested_reviews)
    return reviews


@router.get("/calculate_rating")
def calculate_rating(average_of_ratings: Review_Response,db: Session = Depends(get_db)):
    average = calculate_average_rating(db,average_of_ratings)
    return average

