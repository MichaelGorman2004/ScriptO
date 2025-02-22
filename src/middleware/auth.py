from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
import logging

from src.utils.jwt import JWTHandler
from src.services.user_service import UserService
from src.db.database import get_db_session
from src.utils.logging import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db_session)
) -> UUID:
    """Dependency to get current authenticated user_id"""
    try:
        # Enhanced debug logging
        logger.info("=== Auth Request Debug ===")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Authorization header: {request.headers.get('authorization', 'No Auth header')}")
        logger.info(f"Method: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info("=== End Auth Debug ===")
        
        user_id = JWTHandler.verify_token(token)
        logger.info(f"Token verified for user: {user_id}")
        
        # Verify user exists and is active
        user_service = UserService()
        user = await user_service.get_profile(db, user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=401, detail="User not found")
        if not user.is_active:
            logger.warning(f"User inactive: {user_id}")
            raise HTTPException(status_code=401, detail="User inactive")
            
        return user_id
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Auth error: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        ) 