from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from settings import settings
from dbContext import get_db
from models.models import ProductManager, SalesManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Path to your auth service token endpoint

def verify_pm_role(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Verifying pm role")
        # Decode JWT token using your JWT secret and algorithm
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        print(token)
        
        # Extract user role from token
        role: str = payload.get("role")
        if role != "product_manager":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: Product manager role required"
            )

        email : str = payload.get("sub")
        user = db.query(ProductManager).filter(ProductManager.email == email).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: Product manager role required"
            )
        
        # Optionally, you can add additional checks here (e.g., user status or permissions)
        
    except JWTError:
        raise credentials_exception

    
def verify_sm_role(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Verifying sm role")
        # Decode JWT token using your JWT secret and algorithm
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        print(token)
        
        # Extract user role from token
        role: str = payload.get("role")
        if role != "sales_manager":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: Sales manager role required"
            )

        email : str = payload.get("sub")
        user = db.query(SalesManager).filter(SalesManager.email == email).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: Sales manager role required"
            )
        
        # Optionally, you can add additional checks here (e.g., user status or permissions)
        
    except JWTError:
        raise credentials_exception