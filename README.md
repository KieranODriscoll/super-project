# Full-Stack Application

A modern full-stack application built with React, FastAPI, and PostgreSQL, all containerized with Docker.

## Architecture

- **Frontend**: React 18 with TypeScript, Vite, and Tailwind CSS
- **Backend**: FastAPI with Python 3.11
- **Database**: PostgreSQL 15
- **Containerization**: Docker and Docker Compose

## Features

- Modern React frontend with responsive design
- RESTful API with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Docker containerization for all services
- Hot reloading for development
- Production-ready configuration

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd super-project
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

## Development

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Local Development

**Frontend (React)**
```bash
cd frontend
npm install
npm run dev
```

**Backend (FastAPI)**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

## Project Structure

```
super-project/
├── frontend/                 # React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── backend/                  # FastAPI application
│   ├── app/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── Dockerfile
├── docker-compose.yml        # Main orchestration
├── docker-compose.dev.yml    # Development overrides
└── README.md
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/items` - List all items
- `POST /api/items` - Create new item
- `GET /api/items/{id}` - Get item by ID
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item

**Note:** The backend API runs on port 8001 to avoid conflicts with other services.

## Environment Variables

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_DB=myapp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Backend
DATABASE_URL=postgresql://postgres:password@db:5432/myapp
SECRET_KEY=your-secret-key-here

# Frontend
VITE_API_URL=http://localhost:8000
```

## Production Deployment

For production deployment, use the production Docker Compose configuration:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License