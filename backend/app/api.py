from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from .models import UserLogin, UserRegister, User, UserDB
from .database import get_db, engine
from .auth import verify_password, get_password_hash, create_access_token, get_current_user

from .models import Base
Base.metadata.create_all(bind=engine)

###
# Creates the FastAPI app instance
# This is the entry point and service for handling HTTP requests and responses
###
app = FastAPI()


###
# Defines what domains for the frontend can communicate with the backend
# allow_origins: List of allowed origins that are allowed to access the API
# allow_credentials: Allows the API to send cookies and authentication headers
# allow_methods: List of allowed HTTP methods (GET, POST, PUT, DELETE, etc.)
# allow_headers: List of allowed headers that can be sent in the request
###
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


###
# GET / - Authenticated endpoint
# Defines the root endpoint for the API
# This endpoint is protected and requires a valid JWT token to access
# Depends on the get_current_user function defined in auth.py. If user object is not found
# it will raise an exception and the user will be denied access.
# Returns a welcome message if the user is authenticated.
###
@app.get("/", tags=["root"])
async def read_root(current_user = Depends(get_current_user)):
    return {"message": "Welcome to your full-stack application!"}


###
# GET /api/health - Public endpoint
# This endpoint does not require authentication
# Provides a simple return that the API is up and running
###
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

###
# GET /users/me - Authenticated endpoint
# Depends on the get_current_user function defined in auth.py.
# Returns the current user object if the user is authenticated.
###
@app.get("/users/me")
async def read_user_me(current_user = Depends(get_current_user)):
    return User(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

###
# POST /auth/login - Public endpoint
# Allows the user to authenticate with email and password
# If the user is not found or the password is incorrect, it will raise an exception
# Returns a JWT token if the user exists, password is correct - authentication successful
###
@app.post("/auth/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):

    # Sets the requirement of email and password in the request body
    if not user_credentials.email or not user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
    
    # Queries the DB for the user with the provided email
    user = db.query(UserDB).filter(UserDB.email.ilike(user_credentials.email)).first()

    ###
    # If the user is not found in the DB, raise an exception
    # If the password is not verified, raise an exception
    ###
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Set the user to active in the DB
    if not user.is_active:
        user.is_active = True
        db.commit()
        db.refresh(user)

    # Create a signed JWT token for the user, showing authentication
    access_token = create_access_token(data={"sub": user.email})

    # Provide the JWT token to the user, authenticated till logout or token expires
    return {"access_token": access_token, "token_type": "bearer"}

###
# POST /auth/logout - Authenticated endpoint
# Depends on the get_current_user function defined in auth.py.
# Allows the uesr to logout, setting the is_active flag to False
# Returns a message state logout successful
###
@app.post("/auth/logout")
async def logout(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and set is_active to False"""
    # Set user as inactive upon logout
    current_user.is_active = False
    db.commit()
    
    return {"message": "User logged out successfully"}

###
# GET /auth/logout - Authenticated endpoint
# Depends on the get_current_user function defined in auth.py.
# Allows the uesr to logout, setting the is_active flag to False
# Returns a message state logout successful
###
@app.get("/auth/logout")
async def logout_get(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and set is_active to False"""
    # Set user as inactive upon logout
    current_user.is_active = False
    db.commit()
    
    return {"message": "User logged out successfully"}

###
# POST /auth/register - Public endpoint
# Allows the user to register with an email and password
# Basic input validation + check if the user already exists
# Creates a new user in the DB with hashed password.
# Returns a JWT token, authenticating the user.
###
@app.post("/auth/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Validates that email and password are provided in the request body
    if not user_data.email or not user_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    # Checks the DB for a user with the same email. If found, raise an exception
    existing_user = db.query(UserDB).filter(UserDB.email.ilike(user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Takes the provided plaintext password and hashes it
    # Creates a new UserDB object with the users information
    hashed_password = get_password_hash(user_data.password)
    new_user = UserDB(
        email=user_data.email,
        password=hashed_password,
        is_active=True
    )

    # adds the user to the DB, commits the transaction
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Creates a JWT token for the user, authenticating them
    access_token = create_access_token(data={"sub": new_user.email})
    
    # Returns a succss message and JWT token authenticating the user.
    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }