from sqlalchemy.orm import Session
from models.models import Customer
from utils.jwt_utils import create_access_token, decode_access_token
from utils.hashing_utils import hash_password, verify_password
from fastapi import HTTPException, status


class AuthService:
    '''
        A service class that contains the business logic for the authentication service.
    '''

    # not: Bu fonksiyon frontend çalıştırılmadan istenildiği gibi çalışmaz çünkü frontend çalıştırmadığımızdan log in olan user ın jwt tokenini save edicek bir yer yok.
    @staticmethod
    def check_login_status(token: str, db: Session):
        '''
        Checks the validity of the JWT token and returns user information if valid.

        This function will be called on each homepage load to check if the user is logged in and get the user information for profile page.

        Parameters:
            token (str): The JWT token to be verified.
            db (Session): The SQLAlchemy database session.
        
        Returns:
            dict: A dictionary containing the user information if the token is valid.
                - isLoggedIn (bool): A boolean indicating if the user is logged in.
                - userId (int): The user ID of the logged in user.
                - name (str): The name of the logged in user.
                - surname (str): The surname of the logged in user.
                - email (str): The email of the logged in user.
                - phone_number (str): The phone number of the logged in user.
        '''
        try:
            payload = decode_access_token(token)
            email: str = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(Customer).filter(Customer.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "isLoggedIn": True,
            "userId": user.user_id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "phone_number": user.phone_number
    }


    @staticmethod
    def login(request, db: Session):
        '''
            Function to authenticate a user.
                It queries the database for a user with the given email address and verifies the password.
                If the user is found and the password is correct, the method generates an access token using the create_access_token function from the jwt_utils module.

            Parameters:
                request: LoginRequest - A pydantic model representing the user login request. 
                    - email: EmailStr - The user's email address.
                    - password: str - The user's password.
                db: Session - A SQLAlchemy database session.
            
            Returns:    
                dict: A dictionary containing the access token and token type.
        '''
        user = db.query(Customer).filter(Customer.email == request.email).first()
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        # create access token from the data (user's email) and expiration time and return it to the frontend in the response object
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def register(request, db: Session):
        '''
            Function to register a new user.
                It checks if the user already exists in the database and raises an exception if the user already exists.
                If the user does not exist, the method hashes the password and creates a new Customer object with the user's details.
                The new user is then added to the database and the database session is committed.

            Parameters:
                request: RegisterRequest - A pydantic model representing the user registration request. 
                    - name: str - The user's name.
                    - middlename: str - The user's middle name (optional).
                    - surname: str - The user's surname.
                    - email: EmailStr - The user's email address.
                    - password: str - The user's password.
                    - phone_number: str - The user's phone number (optional).
                db: Session - A SQLAlchemy database session.

            Returns:
                dict: A dictionary containing the registration message and the user_id of the newly registered user
        '''

        existing_user = db.query(Customer).filter(Customer.email == request.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(request.password)
        new_customer = Customer(
            name=request.name,
            middlename=request.middlename,
            surname=request.surname,
            email=request.email,
            password=hashed_password,
            phone_number=request.phone_number
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return {"message": "Registration successful!", "user_id": new_customer.user_id}
