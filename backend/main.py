from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from app.database import get_db, engine
from app.models import Base
from app.schemas import ItemCreate, ItemResponse
from app.crud import create_item, get_items, get_item, update_item, delete_item

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Full-Stack API",
    description="A FastAPI backend for the full-stack application",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Full-Stack API!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/items", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all items with pagination"""
    items = get_items(db, skip=skip, limit=limit)
    return items

@app.post("/api/items", response_model=ItemResponse)
async def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item"""
    return create_item(db=db, item=item)

@app.get("/api/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific item by ID"""
    item = get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/api/items/{item_id}", response_model=ItemResponse)
async def update_existing_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    """Update an existing item"""
    updated_item = update_item(db, item_id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/api/items/{item_id}")
async def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item"""
    success = delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"} 