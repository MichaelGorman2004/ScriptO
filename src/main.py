"""
Main application entry point for ScriptO API.
Configures FastAPI application, middleware, logging, and routes.
"""

from fastapi import FastAPI
from config.settings import settings
from routes.router import api_router
from core.lifecycle import lifespan
from middleware.security import setup_cors, log_request_middleware
from middleware.error_handlers import setup_exception_handlers
from utils.logging import setup_logging

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for ScriptO note-taking and AI assistance platform",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure middleware and error handlers
setup_cors(app)
setup_exception_handlers(app)
app.middleware("http")(log_request_middleware)

# Include routers
app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 