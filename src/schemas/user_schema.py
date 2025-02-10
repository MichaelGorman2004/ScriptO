from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserPreferences(BaseModel):
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