from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from .models import UserLogin, UserRegister, Token, UserResponse, UserDB
from .database import get_db, engine
from .auth import verify_password, get_password_hash, create_access_token, get_current_user

# Create database tables
from .models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["root"])
async def read_root(current_user = Depends(get_current_user)):
    return {"message": "Welcome to your full-stack application!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/users/me")
async def read_user_me(current_user = Depends(get_current_user)):
    return current_user

@app.post("/auth/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):

    user = db.query(UserDB).filter(UserDB.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        user.is_active = True
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/logout")
async def logout(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and set is_active to False"""
    # Set user as inactive upon logout
    current_user.is_active = False
    db.commit()
    
    return {"message": "User logged out successfully"}

# Alternative: GET logout endpoint (if you prefer)
@app.get("/auth/logout")
async def logout_get(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and set is_active to False"""
    # Set user as inactive upon logout
    current_user.is_active = False
    db.commit()
    
    return {"message": "User logged out successfully"}

@app.post("/auth/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = UserDB(
        email=user_data.email,
        password=hashed_password,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create JWT token for the newly registered user
    access_token = create_access_token(data={"sub": new_user.email})
    
    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }