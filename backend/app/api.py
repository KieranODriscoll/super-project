from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
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
async def read_root() -> dict:
    return {"message": "Welcome to your full-stack application!"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.post("/authentication/login")
async def login():
    return {"token": "the token for the user"}

@app.get("/authentication/logout")
async def logout():
    return {"message": "User logged out"}

@app.post("/authentication/register")
async def register():
    return {"message": "User registered"}