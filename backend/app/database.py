from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

###
# Creates a SQLAlchemy ORM to interact with the PostgrSQL database
###

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

###
# Creates a database engine that manages connections to the database
###
engine = create_engine(DATABASE_URL)

###
# Creates a factory for database sessions which handles database transactions
# autocommit=False: The session will not automatically commit transactions
# autoflush=False: The session will not automatically flush changes to the database
# bind=engine: The session will use the engine to connect to the database
###
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

###
# Creates the base for all SQLAlchemy models to inherit fromt
# Provides the found dation for Object Relational Mapping
###
Base = declarative_base()

###
# Helper function to get a database session for use in the API endpoints
###
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 