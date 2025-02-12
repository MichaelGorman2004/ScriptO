Let me provide a comprehensive overview of the project:

### Project Structure Overview

```
src/
├── ai/                     # AI-related functionality
│   ├── config/            # AI configuration settings
│   ├── providers/         # AI service providers (Claude)
│   ├── processors/        # Content/problem processors
│   └── utils/             # AI utilities
├── config/                # Application configuration
│   └── settings.py        # Central settings management
├── db/                    # Database configuration
│   └── database.py        # SQLAlchemy setup
├── models/                # Database models
│   ├── ai_model.py        # AI-related tables
│   ├── note_model.py      # Note-related tables
│   └── user_model.py      # User-related tables
├── schemas/               # Pydantic schemas
│   ├── ai_schema.py       # AI data validation
│   ├── note_schema.py     # Note data validation
│   └── user_schema.py     # User data validation
├── services/             # Business logic
│   ├── ai_service.py     # AI operations
│   ├── base_service.py   # Common service functionality
│   ├── note_service.py   # Note management
│   └── user_service.py   # User management
└── main.py               # Application entry point
```

### Key Components

1. **Database Setup**
- Using PostgreSQL with SQLAlchemy ORM
- Connection string: `postgresql://scripto_user:password@localhost:5432/scripto`
- Migrations handled by Alembic
- Database models in `models/` directory

2. **Models**
- `User`: Authentication and profile
- `UserPreferences`: User settings and preferences
- `Note`: Main note container
- `NoteElement`: Individual note components
- `AIAssistant`: AI-generated content

3. **Services**
- `BaseService`: Common CRUD operations
- `UserService`: User management and auth
- `NoteService`: Note operations
- `AIService`: AI integration

4. **Configuration**
- Environment variables in `.env`
- Pydantic settings management
- Separate configs for development/production

### Database Management

1. **Connection Setup**
```bash
# Create database and user
psql postgres
CREATE DATABASE scripto;
CREATE USER scripto_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE scripto TO scripto_user;
```

2. **Migrations**
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

3. **Database Access (Postico)**
- Host: localhost
- Port: 5432
- Database: scripto
- Username: scripto_user
- Password: password

### Current Status

1. **Completed**
- Database setup and configuration
- Model definitions
- Basic service structure
- Migration system
- Database connection and management

2. **Database Tables Created**
- users
- user_preferences
- notes
- note_elements
- ai_assistants
- alembic_version

### Next Steps

1. **API Development**
- Implement REST endpoints
- Add authentication/authorization
- Set up request/response handling

2. **AI Integration**
- Configure Claude AI provider
- Implement content processing
- Set up AI response handling

3. **Testing**
- Add unit tests
- Set up test database
- Create integration tests

4. **Frontend Integration**
- API documentation
- CORS configuration
- Authentication flow

5. **Deployment**
- Environment configuration
- Database backups
- Logging setup

### Common Operations

1. **Database Operations**
```sql
-- View tables
SELECT * FROM information_schema.tables 
WHERE table_schema = 'public';

-- View table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'users';

-- Create test user
INSERT INTO users (id, email, full_name, is_active)
VALUES (gen_random_uuid(), 'test@example.com', 'Test User', true);
```

2. **Migration Commands**
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

3. **Application Running**
```bash
# Start application
uvicorn src.main:app --reload

# View API docs
http://localhost:8000/docs
```

### Security Considerations

1. **Environment Variables**
- Secure storage of secrets
- Different configs per environment
- No credentials in version control

2. **Database Security**
- Connection pooling
- Password encryption
- Role-based access

3. **API Security**
- JWT authentication
- Rate limiting
- Input validation

### File Details and Relationships

#### Configuration Files
1. `.env`
- Purpose: Environment configuration and secrets
- Used by: `config/settings.py`, `alembic/env.py`
- Contains: Database URL, secret keys, debug flags
- Example:
  ```env
  DATABASE_URL=postgresql://scripto_user:password@localhost:5432/scripto
  SECRET_KEY=your-secret-key
  SQL_DEBUG=true
  ```

2. `alembic/env.py`
- Purpose: Database migration configuration
- Uses: `.env`, all model files
- Used by: Alembic CLI commands
- Key functions:
  - Loads environment variables
  - Imports all models for migration detection
  - Configures database connection
  - Sets up migration context

#### Core Files
1. `src/main.py`
- Purpose: Application entry point
- Uses: 
  - `config/settings.py` for configuration
  - `routes/router.py` for API endpoints
  - `middleware/` for request processing
- Key functions:
  - FastAPI app initialization
  - Middleware setup
  - Route registration
  - Error handling

2. `src/config/settings.py`
- Purpose: Central configuration management
- Uses: `.env`
- Used by: Most application files
- Manages:
  - Database settings
  - API configurations
  - Security settings
  - Feature flags

#### Database Layer
1. `src/db/database.py`
- Purpose: Database connection management
- Uses: `config/settings.py`
- Used by: All models and services
- Provides:
  - SQLAlchemy engine configuration
  - Session management
  - Connection pooling
  - Base model class

#### Models
1. `src/models/user_model.py`
- Purpose: User data structure
- Uses: `db/database.py`
- Used by: 
  - `services/user_service.py`
  - `schemas/user_schema.py`
- Defines:
  ```python
  class User:
      id: UUID
      email: str
      hashed_password: str
      full_name: str
      is_active: bool
      preferences: Relationship[UserPreferences]
      notes: Relationship[Note]
  ```

2. `src/models/note_model.py`
- Purpose: Note data structures
- Uses: 
  - `db/database.py`
  - `models/user_model.py` (for relationships)
- Used by:
  - `services/note_service.py`
  - `schemas/note_schema.py`
- Defines:
  ```python
  class Note:
      id: UUID
      user_id: UUID
      title: str
      content: Relationship[NoteElement]
      created/modified: datetime
  ```

3. `src/models/ai_model.py`
- Purpose: AI interaction data
- Uses: `db/database.py`
- Used by:
  - `services/ai_service.py`
  - `schemas/ai_schema.py`
- Defines: AI assistance records and metadata

#### Services
1. `src/services/base_service.py`
- Purpose: Generic CRUD operations
- Uses: `db/database.py`
- Used by: All other services
- Provides:
  - Create/Read/Update/Delete operations
  - Common query patterns
  - Error handling

2. `src/services/user_service.py`
- Purpose: User management logic
- Uses:
  - `models/user_model.py`
  - `services/base_service.py`
  - `schemas/user_schema.py`
- Provides:
  - User creation/authentication
  - Password hashing
  - Profile management

3. `src/services/note_service.py`
- Purpose: Note management logic
- Uses:
  - `models/note_model.py`
  - `services/base_service.py`
  - `schemas/note_schema.py`
- Provides:
  - Note CRUD operations
  - Element management
  - Version tracking

4. `src/services/ai_service.py`
- Purpose: AI integration logic
- Uses:
  - `models/ai_model.py`
  - `services/base_service.py`
  - `ai/providers/claude_provider.py`
- Provides:
  - AI request handling
  - Response processing
  - Error management

### Workflow Examples

1. **User Creation Flow**
```
Request → main.py
  → routes/user.py
    → services/user_service.py
      → models/user_model.py
        → db/database.py
          → PostgreSQL
```

2. **Note Creation Flow**
```
Request → main.py
  → routes/note.py
    → services/note_service.py
      → models/note_model.py
        → db/database.py
          → PostgreSQL
```

3. **AI Assistance Flow**
```
Request → main.py
  → routes/ai.py
    → services/ai_service.py
      → ai/providers/claude_provider.py
        → Claude API
      → models/ai_model.py
        → db/database.py
          → PostgreSQL
```

4. **Database Migration Flow**
```
alembic revision --autogenerate
  → alembic/env.py
    → models/*
      → db/database.py
        → PostgreSQL
```

### Development Workflow

1. **Adding New Feature**
```
1. Update models/ (if needed)
2. Create migration (alembic revision)
3. Update schemas/
4. Update/create service
5. Add routes
6. Update tests
7. Document changes
```

2. **Database Changes**
```
1. Modify models/
2. Generate migration
3. Test migration
4. Update related services
5. Update tests
6. Apply migration
```

3. **Service Changes**
```
1. Update service logic
2. Update schemas if needed
3. Update tests
4. Update documentation
5. Test endpoints
```
