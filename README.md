# Super Project - Full Stack Application

A modern full-stack web application built with FastAPI backend and React frontend, featuring user authentication, database management, and containerized deployment.

## 🚀 Features

- **Backend API**: FastAPI with PostgreSQL database
- **Frontend**: React with TypeScript and Vite
- **Authentication**: JWT-based user authentication
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Containerization**: Docker Compose for easy deployment
- **Security**: Password hashing with bcrypt
- **CORS**: Configured for cross-origin requests

## 🏗️ Architecture

```
super-project/
├── backend/                 # FastAPI backend application
│   ├── app/                # Application modules
│   │   ├── api.py          # API routes and endpoints
│   │   ├── auth.py         # Authentication logic
│   │   ├── database.py     # Database configuration
│   │   └── models.py       # SQLAlchemy models
│   ├── scripts/            # Database scripts
│   ├── Dockerfile          # Backend container configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend application
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   └── App.tsx         # Main application component
│   ├── Dockerfile          # Frontend container configuration
│   └── package.json        # Node.js dependencies
├── docker-compose.yml      # Multi-container orchestration
├── .env                    # Environment variables
└── README.md              # This file
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Reliable, open-source database
- **SQLAlchemy** - SQL toolkit and ORM
- **JWT** - JSON Web Tokens for authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - JavaScript library for building user interfaces
- **TypeScript** - Typed JavaScript
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd super-project
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:7000
   - API Documentation: http://localhost:7000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example` with the following variables:

#### Database Configuration
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `DATABASE_URL` - Full database connection string
- `DB_HOST` - Database host
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password

#### Backend Configuration
- `SECRET_KEY` - JWT secret key for token signing
- `CORS_ORIGINS` - Comma-separated list of allowed origins

#### Frontend Configuration
- `VITE_API_URL` - Backend API URL

## 📚 API Documentation

### Authentication Endpoints

#### POST /auth/login
Authenticate a user with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### POST /auth/logout
Logout the current user (requires authentication).

### User Endpoints

#### GET /users/me
Get current user information (requires authentication).

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Health Check

#### GET /api/health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for authentication:

1. Users register/login to receive a JWT token
2. Include the token in the `Authorization` header: `Bearer <token>`
3. Protected endpoints validate the token and return user data


## 📁 Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── api.py          # API routes and endpoints
│   ├── auth.py         # Authentication and JWT logic
│   ├── database.py     # Database connection and session
│   └── models.py       # SQLAlchemy models and Pydantic schemas
├── scripts/
│   ├── init.sql        # Database initialization
│   └── seed_database.py # Database seeding
├── Dockerfile          # Backend container configuration
├── main.py             # Application entry point
└── requirements.txt    # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/     # React components
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   └── SignUpPage.tsx
│   ├── App.tsx         # Main application component
│   ├── main.tsx        # Application entry point
│   └── index.css       # Global styles
├── Dockerfile          # Frontend container configuration
├── package.json        # Node.js dependencies
└── vite.config.ts      # Vite configuration
```