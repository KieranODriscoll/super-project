from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# SQLAlchemy Base
Base = declarative_base()

# ============================================================================
# SQLAlchemy ORM Models (Database Tables)
# ============================================================================

class UserDB(Base):
    """SQLAlchemy model for the users table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hashed password
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ============================================================================
# Pydantic Models (API Request/Response)
# ============================================================================

class User(BaseModel):
    """Base user model"""
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

class UserLogin(BaseModel):
    """Request model for login"""
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    """Request model for user registration"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Response model for JWT token"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Model for JWT token payload"""
    email: Optional[str] = None

class UserResponse(BaseModel):
    """Response model for user data"""
    id: int
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model

class UserCreate(BaseModel):
    """Model for creating a new user"""
    email: EmailStr
    password: str

