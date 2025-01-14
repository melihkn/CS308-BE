from jose import jwt, JWTError
from datetime import datetime, timedelta

# Secret key to encode and decode JWT tokens
SECRET_KEY = "e8e7e4"
# Algorithm used to encode and decode JWT tokens (HS256 = HMAC with SHA-256)
ALGORITHM = "HS256"
# Expiration time for the access token in minutes (30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 1000


def create_access_token(data: dict, expires_delta: timedelta = None):
    '''
    Creates a JWT access token with the given data (user's email for our use case) and expiration time.
    '''
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    '''
    Decodes a JWT token and returns the payload if valid.
    Raises an exception if the token is invalid or expired.
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise e