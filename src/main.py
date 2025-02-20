"""
Main application entry point for ScriptO API.
Configures FastAPI application, middleware, logging, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from src.routes.router import api_router
from src.core.lifecycle import lifespan
from src.middleware.security import setup_cors, log_request_middleware
from src.middleware.error_handlers import setup_exception_handlers
from src.utils.logging import setup_logging

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for ScriptO note-taking and AI assistance platform",
    version=settings.VERSION,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure middleware and error handlers
setup_cors(app)
setup_exception_handlers(app)
app.middleware("http")(log_request_middleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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