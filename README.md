# ScriptO API

## ⚠️ License Notice

```
Copyright (c) 2025 Michael Gorman
All rights reserved.

This code is made public for viewing and educational purposes only.
No permission is granted for any use, modification, or distribution
without explicit written permission from the copyright holder.
```

A FastAPI-based backend for the ScriptO note-taking and AI assistance platform.

## Features

- JWT-based authentication
- STEM problem solving with Claude AI
- Note management with rich content support
- User preference management
- Rate limiting
- Background task processing
- Standardized API responses
- PostgreSQL database with SQLAlchemy ORM

## Project Structure
```
src/
├── ai/                     # AI-related functionality
│   ├── config/            # AI configuration settings
│   ├── providers/         # AI service providers (Claude)
│   └── processors/        # Content processors
├── config/                # Application configuration
│   └── settings.py        # Central settings management
├── core/                  # Core application components
│   └── lifecycle.py       # Application lifecycle management
├── db/                    # Database configuration
│   └── database.py        # SQLAlchemy setup
├── middleware/            # Middleware components
│   ├── auth.py           # Authentication middleware
│   ├── error_handlers.py # Error handling
│   ├── rate_limiter.py  # Rate limiting
│   └── security.py      # Security middleware
├── models/               # Database models
│   ├── ai_model.py      # AI-related tables
│   ├── note_model.py    # Note-related tables
│   └── user_model.py    # User-related tables
├── routes/              # API routes
│   ├── ai_route.py     # AI endpoints
│   ├── auth_route.py   # Authentication endpoints
│   ├── note_route.py   # Note management
│   └── user_route.py   # User management
├── schemas/            # Pydantic schemas
│   ├── ai_schema.py   # AI data validation
│   ├── note_schema.py # Note data validation
│   └── user_schema.py # User data validation
├── services/          # Business logic
│   ├── ai_service.py # AI operations
│   ├── note_service.py # Note management
│   └── user_service.py # User management
└── main.py           # Application entry point
```

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
# Create database and user
psql postgres
CREATE DATABASE scripto;
CREATE USER scripto_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE scripto TO scripto_user;
```

4. Set up environment variables:
```bash
# Copy the example env file and update with your values
cp .env.example .env
```

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn src.main:app --reload
```

## API Documentation

- Interactive API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/api/v1/openapi.json
- Detailed documentation: [API_Documentation.md](API_Documentation.md)

## Authentication

The API uses JWT tokens for authentication. Protected endpoints require a Bearer token:
```
Authorization: Bearer <jwt_token>
```

## Rate Limiting

- AI Routes: 30 requests/minute
- Note Routes: 60 requests/minute
- User Routes: 30 requests/minute

## Response Format

All endpoints return responses in the following format:
```json
{
    "success": boolean,
    "message": string,
    "data": any,
    "metadata": {
        "timestamp": datetime,
        "version": string
    }
}
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black src/
isort src/
```

4. Run linting:
```bash
flake8 src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

