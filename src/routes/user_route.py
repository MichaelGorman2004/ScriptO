from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from ..schemas.user_schema import UserCreate, UserUpdate, UserProfile, UserPreferences
from ..services.user_service import UserService
from ..utils.response import APIResponse
from ..utils.logging import logger
from ..middleware.rate_limiter import RateLimiter
from ..middleware.auth import get_current_user
from ..db.database import get_db_session

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=30)
user_service = UserService()

@router.post("/register", response_model=APIResponse)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db_session)
):
    """Register a new user"""
    try:
        logger.info("New user registration request")
        created_user = await user_service.create_user(db, user)
        
        return APIResponse(
            success=True,
            message="User registered successfully",
            data=created_user,
            metadata={
                "timestamp": datetime.now(UTC)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/profile", response_model=APIResponse)
async def get_profile(
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Get user profile"""
    try:
        profile = await user_service.get_profile(db, current_user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        return APIResponse(
            success=True,
            message="Profile retrieved successfully",
            data=profile
        )
    except Exception as e:
        logger.error(f"Profile retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve profile")

@router.put("/profile", response_model=APIResponse)
async def update_profile(
    profile: UserUpdate,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Update user profile"""
    try:
        updated_profile = await user_service.update_profile(db, current_user_id, profile)
        
        return APIResponse(
            success=True,
            message="Profile updated successfully",
            data=updated_profile
        )
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

@router.put("/preferences", response_model=APIResponse)
async def update_preferences(
    preferences: UserPreferences,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Update user preferences"""
    try:
        updated_prefs = await user_service.update_preferences(db, current_user_id, preferences)
        
        return APIResponse(
            success=True,
            message="Preferences updated successfully",
            data=updated_prefs
        )
    except Exception as e:
        logger.error(f"Preferences update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

@router.post("/change-password", response_model=APIResponse)
async def change_password(
    current_password: str,
    new_password: str,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Change user password"""
    try:
        success = await user_service.change_password(db, current_user_id, current_password, new_password)
        
        return APIResponse(
            success=True,
            message="Password changed successfully"
        )
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to change password")

@router.delete("/deactivate", response_model=APIResponse)
async def deactivate_account(
    password: str,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Deactivate user account"""
    try:
        success = await user_service.deactivate_account(db, current_user_id, password)
        
        return APIResponse(
            success=True,
            message="Account deactivated successfully"
        )
    except Exception as e:
        logger.error(f"Account deactivation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deactivate account")