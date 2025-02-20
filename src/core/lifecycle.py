from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings
from src.db.database import Base, engine

logger = logging.getLogger("scripto")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifecycle manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up ScriptO API")
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down ScriptO API")
    # Add cleanup here if needed 