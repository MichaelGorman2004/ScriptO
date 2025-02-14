from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from src.utils.jwt import JWTHandler
from src.services.user_service import UserService
from src.db.database import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db_session)
) -> UUID:
    """Dependency to get current authenticated user_id"""
    try:
        user_id = JWTHandler.verify_token(token)
        
        # Verify user exists and is active
        user_service = UserService(db)
        user = await user_service.get_profile(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="User not found or inactive"
            )
            
        return user_id
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        ) 