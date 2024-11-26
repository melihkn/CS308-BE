from fastapi import APIRouter, Depends, HTTPException, status
# importing Session from sqlalchemy.orm module
from sqlalchemy.orm import Session
# importing Customer model from models module
from models.models import Customer
# importing AuthService class from services.auth_service module
from services.auth_service import AuthService
# importing get_db function from utils.db_utils module to get the database session  
from utils.db_utils import get_db
# these are four classes from pydantic module that are used to define request and response models for the login and register endpoints
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    middlename: str = None
    surname: str
    email: EmailStr
    password: str
    phone_number: str = None

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # without creating an instance of the AuthService class, we can call the login method directly using the class name because it is a static method
    return AuthService.login(request, db) # it will retrun a json object with includes access_token and token_type

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # just give the pydantic class instance and the database session to the register method.
    return AuthService.register(request, db) # it will return a json object with includes message and user_id

# OAuth2PasswordBearer is a class from fastapi.security module that is used to define the OAuth2 password bearer token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/auth/status")
async def check_login_status(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Endpoint to check if the user is logged in by verifying the JWT token.
    Calls the AuthService to handle the logic.
    """
    return AuthService.check_login_status(token, db)