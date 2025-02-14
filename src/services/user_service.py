"""
User Service Module

This module handles all user-related operations including authentication,
profile management, and preferences.
"""

from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from passlib.context import CryptContext

from src.models.user_model import User, UserPreferences
from src.schemas.user_schema import UserCreate, UserUpdate, UserProfile
from src.services.base_service import BaseService
from src.utils.logging import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for handling user-related operations."""
    
    def __init__(self, db: Session):
        super().__init__(model=User, db=db)
        
    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user with hashed password"""
        try:
            # Check if email exists
            if self.db.query(User).filter(User.email == user_create.email).first():
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # Hash password
            user_data = user_create.model_dump()
            user_data["hashed_password"] = self._get_password_hash(user_data.pop("password"))
            user_data["created_at"] = datetime.now(UTC)
            
            user = User(**user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_profile(self, user_id: UUID) -> Optional[User]:
        """Get user profile by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    async def update_profile(self, user_id: UUID, profile: UserUpdate) -> User:
        """Update user profile"""
        user = await self.get_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        update_data = profile.model_dump(exclude_unset=True)
        
        # Handle password update separately
        if "password" in update_data:
            update_data["hashed_password"] = self._get_password_hash(update_data.pop("password"))
            
        for field, value in update_data.items():
            setattr(user, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_preferences(self, user_id: UUID, preferences: UserPreferences) -> User:
        """Update user preferences"""
        user = await self.get_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if not user.preferences:
            user.preferences = UserPreferences(user_id=user_id)
            
        pref_data = preferences.model_dump()
        for field, value in pref_data.items():
            setattr(user.preferences, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    async def change_password(self, user_id: UUID, current_password: str, new_password: str) -> bool:
        """Change user password"""
        user = await self.get_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if not self._verify_password(current_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
            
        user.hashed_password = self._get_password_hash(new_password)
        
        try:
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    async def deactivate_account(self, user_id: UUID, password: str) -> bool:
        """Deactivate user account"""
        user = await self.get_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if not self._verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
            
        user.is_active = False
        
        try:
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    
    def _get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return None
            
            if not self._verify_password(password, user.hashed_password):
                return None
            
            return user
        
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None 