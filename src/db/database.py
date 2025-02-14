from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
from fastapi import Depends
from src.config.settings import settings

# Create engine with connection pool settings
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.SQL_DEBUG
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for FastAPI endpoints
db_dependency = Depends(get_db)

@contextmanager
def get_db_context():
    """Context manager for database sessions (for scripts/tasks)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 