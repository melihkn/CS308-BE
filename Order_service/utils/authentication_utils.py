from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from Order_service.utils.order_settings import settings
from utils.db_utils import get_db
from models.models import Customer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Path to your auth service token endpoint


#this function verifies if the given token is user role token or not
def verify_user_role(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Verifying user")
        # Decode JWT token using your JWT secret and algorithm
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        print(token)
        
        # Extract user role from token
        role: str = payload.get("role")
        if role != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: customer role required"
            )

        email : str = payload.get("sub")
        user = db.query(Customer).filter(Customer.email == email).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: This customer does not exist"
            )
        
        # Optionally, you can add additional checks here (e.g., user status or permissions)
        
    except JWTError:
        raise credentials_exception
