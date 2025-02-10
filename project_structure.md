scripto/
├── src/
│   ├── main.py                  # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuration settings
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── router.py          # Main router that combines all routes
│   │   ├── notes_route.py     # Notes endpoints
│   │   ├── ai_route.py        # AI endpoints
│   │   └── users_route.py     # Users endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py          # Authentication and security
│   │   └── exceptions.py        # Custom exceptions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── note.py             # Note-related models
│   │   ├── user.py             # User-related models
│   │   └── ai.py               # AI-related models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── note.py             # Pydantic models for notes
│   │   ├── user.py             # Pydantic models for users
│   │   └── ai.py               # Pydantic models for AI
│   ├── services/
│   │   ├── __init__.py
│   │   ├── note_service.py     # Note business logic
│   │   ├── ai_service.py       # AI processing logic
│   │   └── user_service.py     # User management logic
│   └── db/
│       ├── __init__.py
│       └── database.py         # Database connection and models
├── tests/
│   ├── __init__.py
│   ├── test_notes.py
│   ├── test_ai.py
│   └── test_users.py
├── requirements.txt
└── README.md 