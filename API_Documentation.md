# ScriptO API Documentation

## ⚠️ License Notice

```
Copyright (c) 2025 Michael Gorman
All rights reserved.

This documentation and associated code are made public for viewing 
and educational purposes only. No permission is granted for any use,
modification, or distribution without explicit written permission
from the copyright holder.
```

## Overview
ScriptO is a note-taking and AI assistance platform that provides STEM problem-solving and term definition capabilities.

- Base URL: `http://localhost:8000`
- API Version: v1
- Base Path: `/api/v1`

## Authentication

### JWT Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Login
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "access_token": "jwt_token_here",
        "token_type": "bearer"
    },
    "metadata": {
        "expires_in": 1800,
        "timestamp": "2024-03-15T12:00:00Z"
    }
}
```

## User Management

### Register New User
```http
POST /api/v1/users/register
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "secure_password"
}
```

### Get User Profile
```http
GET /api/v1/users/profile
```
Protected: Yes

### Update User Profile
```http
PUT /api/v1/users/profile
```

**Request Body:**
```json
{
    "email": "new@example.com",
    "full_name": "Updated Name"
}
```

### Update User Preferences
```http
PUT /api/v1/users/preferences
```

**Request Body:**
```json
{
    "learning_preferences": {},
    "ai_settings": {},
    "theme": "dark",
    "notifications_enabled": true
}
```

### Change Password
```http
POST /api/v1/users/change-password
```

**Query Parameters:**
- `current_password`: string
- `new_password`: string

### Deactivate Account
```http
DELETE /api/v1/users/deactivate
```

**Query Parameters:**
- `password`: string

## Note Management

### Create Note
```http
POST /api/v1/notes/
```

**Request Body:**
```json
{
    "title": "string",
    "tags": ["tag1", "tag2"],
    "subject": "string",
    "content": [
        {
            "type": "text",
            "content": {},
            "bounds": {},
            "stroke_properties": {}
        }
    ]
}
```

### Get Note
```http
GET /api/v1/notes/{note_id}
```

### Update Note
```http
PUT /api/v1/notes/{note_id}
```

**Request Body:**
```json
{
    "title": "string",
    "tags": ["tag1", "tag2"],
    "subject": "string",
    "content": []
}
```

### Delete Note
```http
DELETE /api/v1/notes/{note_id}
```

### List Notes
```http
GET /api/v1/notes/
```

**Query Parameters:**
- `skip`: integer (default: 0)
- `limit`: integer (default: 100)

### Add Note Element
```http
POST /api/v1/notes/{note_id}/elements
```

**Request Body:**
```json
{
    "type": "string",
    "content": {},
    "bounds": {},
    "stroke_properties": {}
}
```

### Search Notes
```http
GET /api/v1/notes/search
```

**Query Parameters:**
- `query`: string (required)
- `sort_by`: string (default: "modified")
- `sort_order`: string (default: "desc")
- `skip`: integer (default: 0)
- `limit`: integer (default: 100)

### Bulk Delete Notes
```http
DELETE /api/v1/notes/bulk
```

**Request Body:**
```json
{
    "note_ids": ["uuid1", "uuid2"]
}
```

## AI Features

### Solve STEM Problem
```http
POST /api/v1/ai/solve
```

**Request Body:**
```json
{
    "problem": "string",
    "subject": "string",
    "context": {}
}
```

**Rate Limit:** 30 requests/minute

### Define Term
```http
POST /api/v1/ai/define
```

**Request Body:**
```json
{
    "term": "string",
    "context": {}
}
```

**Rate Limit:** 30 requests/minute

### Check AI Status
```http
GET /api/v1/ai/status/{interaction_id}
```

**Response:**
```json
{
    "success": true,
    "message": "Status retrieved successfully",
    "data": {},
    "metadata": {
        "status": "completed",
        "created_at": "2024-03-15T12:00:00Z",
        "completed_at": "2024-03-15T12:00:05Z"
    }
}
```

## Common Response Format
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

## Error Handling

### Error Response Format
```json
{
    "success": false,
    "message": "Error description",
    "data": null,
    "metadata": {
        "timestamp": datetime,
        "error_type": string
    }
}
```

### Common Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

### Error Types
- `ai_error`: AI-related processing errors
- `database_error`: Database operation failures
- `authentication_error`: Authentication/authorization issues
- `validation_error`: Input validation failures

## Rate Limiting
- AI Routes: 30 requests/minute
- Note Routes: 60 requests/minute
- User Routes: 30 requests/minute

### Rate Limit Response
```json
{
    "success": false,
    "message": "Too many requests. Please try again later.",
    "metadata": {
        "timestamp": datetime
    }
}
```

## CORS Configuration
The API allows cross-origin requests with the following configuration:
- Allowed Origins: http://localhost:3000
- Methods: GET, POST, PUT, DELETE, PATCH
- Headers: Authorization, Content-Type
- Credentials: Allowed

## Database Models

### User
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP
);
```

### Note
```sql
CREATE TABLE notes (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR,
    created TIMESTAMP,
    modified TIMESTAMP,
    tags JSON,
    subject VARCHAR
);
```

### AI Interaction
```sql
CREATE TABLE ai_interactions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    type VARCHAR,
    status VARCHAR,
    request_data JSON,
    response_data JSON,
    error_message VARCHAR,
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

## Health Check
```http
GET /health
```

**Response:**
```json
{
    "status": "healthy"
}
```

## API Versioning
The API uses URL versioning with the format: `/api/v{version_number}`
Current version: v1

## Additional Resources
- Interactive API Documentation: `/docs`
- OpenAPI Specification: `/api/v1/openapi.json`
- Source Code: [GitHub Repository]

## Development Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://scripto_user:password@localhost:5432/scripto
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
CLAUDE_API_KEY=your-claude-api-key
```

3. Run migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn src.main:app --reload
```
