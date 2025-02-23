from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.config.settings import settings
import logging

logger = logging.getLogger("scripto")

def setup_security(app: FastAPI):
    """Configure security middleware and settings"""
    # Disable automatic redirect for trailing slashes
    app.router.redirect_slashes = False
    
    # Add compression for large responses
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type"],
    )

async def log_request_middleware(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    if response.status_code in [301, 302, 307, 308]:
        logger.info(f"Redirect location: {response.headers.get('location')}")
    return response 