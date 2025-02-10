"""
User Schema Definitions for the API

This module defines the Pydantic models for user-related data validation and serialization.
It includes schemas for user creation, updates, preferences, and profile information.

Key Components:
- UserBase: Base schema containing common user properties
- UserCreate: Schema for new user registration
- UserUpdate: Schema for updating user information
- UserPreferences: Schema for user-specific preferences and settings
- UserProfile: Complete user profile schema with all user information
"""

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Base schema for user information.
    
    Attributes:
        email (EmailStr): User's email address, validated as proper email format
        full_name (str): User's full name
    """
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserPreferences(BaseModel):
    """
    Schema for user preferences and settings.
    
    Attributes:
        learning_preferences (dict): User's learning style and preferences
        ai_settings (dict): AI-related customization settings
        theme (str): UI theme preference
        notifications_enabled (bool): Whether notifications are enabled
    """
    learning_preferences: dict
    ai_settings: dict
    theme: str
    notifications_enabled: bool

class UserProfile(UserBase):
    id: UUID
    is_active: bool
    preferences: Optional[UserPreferences] = None

    class Config:
        from_attributes = True 