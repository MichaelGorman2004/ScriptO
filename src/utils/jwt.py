from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import JWTError, jwt
from uuid import UUID
from fastapi import HTTPException

from src.config.settings import settings

class JWTHandler:
    """Handles JWT token creation and validation"""
    
    SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @classmethod
    def create_access_token(cls, user_id: UUID) -> str:
        """Create JWT access token"""
        expires_delta = timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        expire = datetime.now(UTC) + expires_delta
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
    
    @classmethod
    def verify_token(cls, token: str) -> UUID:
        """Verify JWT token and return user_id"""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication credentials"
                )
            return UUID(user_id)
            
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            ) 