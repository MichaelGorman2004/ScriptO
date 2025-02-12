from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging
from utils.exceptions import AIError, DatabaseError, AuthenticationError

logger = logging.getLogger("scripto")

def setup_exception_handlers(app):
    """Configure exception handlers"""
    
    @app.exception_handler(AIError)
    async def ai_error_handler(request: Request, exc: AIError):
        logger.error(f"AI Error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc), "type": "ai_error"}
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        logger.error(f"Database Error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc), "type": "database_error"}
        )

    @app.exception_handler(AuthenticationError)
    async def auth_error_handler(request: Request, exc: AuthenticationError):
        logger.error(f"Authentication Error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc), "type": "authentication_error"}
        ) 