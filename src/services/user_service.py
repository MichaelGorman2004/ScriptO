"""
User Service Module

This module handles all user-related operations including user management,
authentication, and user preferences handling.

Key Features:
- User CRUD operations
- Password hashing and verification
- User preference management
- Authentication checks
"""

from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserUpdate, UserPreferences
from src.services.base_service import BaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """
    Service for handling user-related operations.
    
    Extends the BaseService with user-specific functionality including
    authentication and preference management.
    """
    
    def __init__(self, db: Session):
        super().__init__(model=User, db=db)
        
    async def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user with hashed password.
        
        Args:
            user_create: UserCreate schema containing user data
            
        Returns:
            Created user instance
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == user_create.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        # Hash password
        hashed_password = self._get_password_hash(user_create.password)
        user_data = user_create.model_dump()
        user_data["hashed_password"] = hashed_password
        del user_data["password"]
        
        return await super().create(UserCreate(**user_data))
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        
        Args:
            email: User's email
            password: Plain text password
            
        Returns:
            Authenticated user or None
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not self._verify_password(password, user.hashed_password):
            return None
        return user
    
    async def update_preferences(self, user_id: UUID, preferences: UserPreferences) -> User:
        """
        Update user preferences.
        
        Args:
            user_id: UUID of the user
            preferences: New preferences data
            
        Returns:
            Updated user instance
            
        Raises:
            HTTPException: If user not found
        """
        user = await self.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user.preferences = preferences.model_dump()
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def change_password(self, user_id: UUID, current_password: str, new_password: str) -> bool:
        """
        Change user's password.
        
        Args:
            user_id: UUID of the user
            current_password: Current password for verification
            new_password: New password to set
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If current password is invalid or user not found
        """
        user = await self.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if not self._verify_password(current_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid current password")
            
        user.hashed_password = self._get_password_hash(new_password)
        self.db.commit()
        return True
    
    def _get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return pwd_context.verify(plain_password, hashed_password) 