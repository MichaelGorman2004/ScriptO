from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from db.database import Base, engine

logger = logging.getLogger("scripto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifecycle events"""
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