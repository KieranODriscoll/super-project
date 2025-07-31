from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

Base = declarative_base()

###
# User model for databse table, maps python objects to rows, handles CRUD operations

# id: Primary key, increments, primary key
# email: string, unique, not null
# password: string, not null, hash value
# is_active: boolean, default false
# created_at: datetime, default now
# updated_at: datetime, default now
###
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hashed password
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


###
# Pydantic models - Define the data structure, enforce validation rules
###

###
# User model - defines the data structure of a user.
# Used in response for when /users/me is called
# id: int, the user's identifier
# email: EmailStr, user's email address validated by EmailStr
# is_active: bool, whether the user is logged in or not (does not mean JWT is not expired)
# created_at: datetime, the date and time the user was created
# updated_at: datetime, the date and time the user was last updated
###
class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

###
# UserLogin model - defines the data structure for a user log in request
# email: EmailStr, user's email address validated by EmailStr
# password: str, user's password
###
class UserLogin(BaseModel):
    email: EmailStr
    password: str

###
# UserRegister model - defines the data structure for a user registration request
# email: EmailStr, user's email address validated by EmailStr
# password: str, user's password
###
class UserRegister(BaseModel):
    email: EmailStr
    password: str

###
# Token model - defines the data structure for a JWT token response
# access_token: str, the JWT token
# token_type: str, the type of token (Bearer)
###
class Token(BaseModel):
    access_token: str
    token_type: str

###
# TokenData model - defines the data structure for a JWT token payload
# This is optional informtion added to the JWT
# email: Optional[str], the user's email address,
###
class TokenData(BaseModel):
    email: Optional[str] = None
