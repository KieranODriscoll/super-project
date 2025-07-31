import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import TokenData, UserDB
from sqlalchemy.orm import Session
from .database import get_db

# Configuration
###
# Set JWT secret key, algorithm, and expiration time
# The key and algorithm are used to sign and verify the JWT token
# The expiration time is the duration of the token's validity
###
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

###
# CryptoContext is a helper for hashing passwords using different algorithms.
# In this case, we will use bcrypt, which is consider secure for password hashing.
# IT also allows for the verification of a plaintext password against a hashed password.
###
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Defines the security scheme for the API, using bearer for authentication
security = HTTPBearer()


###
# Verifies the plaintext password against the hashed password using
# the pwd_context defined earlier and bcrypt.
###
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

###
# Hashes a plaintext password using the pwd_context defined earlier and bcrypt.
###
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

###
# Creates a JWT access token using the JWT library.
# Encodes it using the SECRET_KEY and provided algorithm
# Computes a expiration time based on the defined expiration time (5 minutes)
# Data contains the email of the user
# Returns the encoded JWT token
###
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

###
# Verifies the JWT token is still valid using the JWT library.
# If the token has been tampered with, it will be invalid and raise an exeception
# If the token has expired, it will be invalid and raise an exception
# Return the email within the token, if the token is valid.
###
def verify_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        expire = payload.get("exp")
        if expire is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
        return token_data
    except JWTError as e:
        if "expired" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise credentials_exception

###
# Gets the current user from the JWT token.
# This function is used in a protected API endpoint, to validate the user is authenticated.
# It uses the HTTPAuthorizationCredentials to get the token from the request header.
# It then verifies the token is valid using the verify_token function.
# If the token is invalid, it raises an exception.
# Returns the user object if the token is valid.
### 
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data.email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(UserDB).filter(UserDB.email == token_data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )

    return user
