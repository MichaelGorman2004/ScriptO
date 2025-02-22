from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, UTC

from src.services.user_service import UserService
from src.utils.jwt import JWTHandler
from src.utils.response import APIResponse
from src.utils.logging import logger
from src.db.database import get_db_session

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_db_session)
):
    """Login user and return JWT token"""
    try:
        # Enhanced debug logging
        logger.info("Login request received")
        logger.info(f"Request form data: {form_data.__dict__ if hasattr(form_data, '__dict__') else 'No form data'}")
        logger.info(f"Username present: {hasattr(form_data, 'username')}")
        logger.info(f"Password present: {hasattr(form_data, 'password')}")
        
        user_service = UserService()
        user = await user_service.authenticate_user(
            db=db,
            email=form_data.username,
            password=form_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
            
        access_token = JWTHandler.create_access_token(user.id)
        
        return APIResponse(
            success=True,
            message="Login successful",
            data={
                "access_token": access_token,
                "token_type": "bearer"
            },
            metadata={
                "timestamp": datetime.now(UTC),
                "expires_in": JWTHandler.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed") 