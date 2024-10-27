from passlib.context import CryptContext
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import hashlib
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, EmailStr
from classes import *  # Import the classes, functions, and variables explicitly defined in the classes.py
from jose import jwt, JWTError
from datetime import datetime, timedelta
# this is for the frontend to be able to send requests to the backend
from fastapi.middleware.cors import CORSMiddleware
# this is for the JWT token to be able to authenticate the user
from fastapi.security import OAuth2PasswordBearer

# JWT configuration
SECRET_KEY = "e8e7e4"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # token will expire in 30 minutes (base minutes)

# simpler hashing and verifying functions
def hash_password(password: str) -> str:
    # Encode the password to bytes and hash it using SHA-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Hash the plain password (typed password in the UI) and compare with the stored hashed password which is hashed
    return hash_password(plain_password) == hashed_password

# to use the token in the requests to authenticate the user (frontend)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    '''
        Function to create a JWT access token. The token contains encoded user data and an expiration time.

        Parameters:
            - data: A dictionary of data (usually user details) to be encoded into the token.
            - expires_delta: Expiration time of the token (default is 30 minutes)
        Returns:
            - JWT access token
    '''
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the frontend on port 3003
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],
)


# SQLAlchemy setup
DATABASE_URL = "mysql+pymysql://root:TunahanTunahan987.%2C@127.0.0.1:3306/CS308_Project"
engine = create_engine(DATABASE_URL)
# to make changes on the real database (local) -> we need to create a session
SessionLocal = sessionmaker( bind=engine)

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Pydantic model for registration request
class RegisterRequest(BaseModel):
    name: str
    middlename: str = None
    surname: str
    email: EmailStr
    password: str
    phone_number: str = None


@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    '''
        Authenticate user and generate JWT token.

        Parameters:
            - request: LoginRequest model containing email and password
            - db: Database session dependency

        Returns:
            - JWT token if the user is authenticated successfully as in the form of {"access_token ": "token", "token_type": "bearer"}
    '''
    '''
        This is the endpoint for the user to login and get a JWT token to be able to access protected routes.

        How to use?

        Frontend sends a POST request to the /login endpoint 
        which has the address: http://127.0.0.1:8000/login
        it means:
            - host of the server is 127.0.0.1
            - port of the server is 8000 
            - endpoint is /login

        with the following JSON body
        {
            "email": "
            "password": "
        }
    '''

    user = db.query(Customer).filter(Customer.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Create a JWT token with user email
    access_token = create_access_token(data={"sub": user.email})

    # return the token to the user (frontend) to store it in the local storage or in the cookies
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint for registration
@app.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(Customer).filter(Customer.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = hash_password(request.password)
    
    # Create a new customer instance
    new_customer = Customer(
        name=request.name,
        middlename=request.middlename,
        surname=request.surname,
        email=request.email,
        password=hashed_password,
        phone_number=request.phone_number
    )
    
    # Add the new customer to the database (db is the session)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {"message": "Registration successful!", "user_id": new_customer.user_id}

# to test database connection, lets select every customer
@app.get("/test")
def test(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers


@app.get("/users/me")
async def get_user_me(token: str = Depends(oauth2_scheme)):
    """Retrieve the current logged-in user using JWT token."""
    '''
        An endpoint that verifies the JWT token, extracts the user’s email from it, and returns it if valid.

        Usage: This function is useful in applications where users need to verify their 
        login status or request their profile information securely via JWT tokens. 
        If the token is valid, the user’s email is returned; if not, a 401 Unauthorized error is raised.

        Our usage: Frontend sends a GET request to the /users/me endpoint to 
        authenticate the user. The token is sent in the Authorization header.

        parameters:
            - token: JWT token sent by the frontend in the Authorization header
    
        returns:
            - email: email of the user decoded from the token
    '''
    try:
        # decode the token and get the email (only email is used to create the token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # get the email from the payload which is decoded from the token 
        email: str = payload.get("sub")
        # if email is None, raise an exception which means user is not authenticated (logged in)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # if user correctly authenticated, return the email to the user (frontend)
    return {"email": email}


# a protected route to see user profile
@app.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Protected route to fetch user profile information. Meaning, it can visible only if the user is authenticated.

    params:
        - token: JWT token sent by the frontend in the Authorization header
        - db: Database session dependency

    returns:
        - User profile information (user_id, name, surname, email, phone_number if exists)
    
    """
    try:
        # Decode the JWT token to get the email
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Get the email from the payload (jwt token is created only by using email)
        email: str = payload.get("sub") # payload is the decoded token and sub is the email
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Query user information from the database using email
    user = db.query(Customer).filter(Customer.email == email).first()
    
    # if user is not found, raise an exception
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return user profile information in JSON format to the frontend to display
    return {
        "user_id": user.user_id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "phone_number": user.phone_number
    }


'''
users:
t@gmail.com - 19482011
b@gmail.com - 123456


to run the app: uvicorn main:app --reload
'''
