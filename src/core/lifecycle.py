from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger("scripto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifecycle events"""
    # Startup
    logger.info("Starting up ScriptO API")
    # Add any startup initialization here (DB connections, caches, etc.)
    yield
    # Shutdown
    logger.info("Shutting down ScriptO API")
    # Add any cleanup here 