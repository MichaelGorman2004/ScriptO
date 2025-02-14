from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Optional
from uuid import UUID
from datetime import datetime, UTC

from ..schemas.user_schema import UserCreate, UserUpdate, UserProfile, UserPreferences
from ..services.user_service import UserService
from ..utils.response import APIResponse
from ..utils.logging import logger
from ..middleware.rate_limiter import RateLimiter

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=30)

@router.post("/register", response_model=APIResponse)
async def register_user(user: UserCreate):
    """Register a new user"""
    try:
        logger.info("New user registration request")
        created_user = await UserService.create_user(user)
        
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
async def get_profile(user_id: UUID):  # Will come from JWT auth later
    """Get user profile"""
    try:
        profile = await UserService.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        return APIResponse(
            success=True,
            message="Profile retrieved successfully",
            data=profile
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve profile")

@router.put("/profile", response_model=APIResponse)
async def update_profile(
    user_id: UUID,  # Will come from JWT auth later
    profile: UserUpdate
):
    """Update user profile"""
    try:
        updated_profile = await UserService.update_profile(user_id, profile)
        
        return APIResponse(
            success=True,
            message="Profile updated successfully",
            data=updated_profile
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

@router.put("/preferences", response_model=APIResponse)
async def update_preferences(
    user_id: UUID,  # Will come from JWT auth later
    preferences: UserPreferences
):
    """Update user preferences"""
    try:
        updated_prefs = await UserService.update_preferences(user_id, preferences)
        
        return APIResponse(
            success=True,
            message="Preferences updated successfully",
            data=updated_prefs
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Preferences update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

@router.post("/change-password", response_model=APIResponse)
async def change_password(
    user_id: UUID,  # Will come from JWT auth later
    current_password: str,
    new_password: str
):
    """Change user password"""
    try:
        success = await UserService.change_password(
            user_id,
            current_password,
            new_password
        )
        
        return APIResponse(
            success=True,
            message="Password changed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to change password")

@router.delete("/deactivate", response_model=APIResponse)
async def deactivate_account(
    user_id: UUID,  # Will come from JWT auth later
    password: str
):
    """Deactivate user account"""
    try:
        success = await UserService.deactivate_account(user_id, password)
        
        return APIResponse(
            success=True,
            message="Account deactivated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Account deactivation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deactivate account")