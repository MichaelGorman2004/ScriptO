from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Column, DateTime, String, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from src.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True))
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    notes = relationship("Note", back_populates="user")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(PGUUID, primary_key=True, index=True)
    user_id = Column(PGUUID, ForeignKey("users.id"))
    learning_preferences = Column(JSON)
    ai_settings = Column(JSON)
    theme = Column(String)
    notifications_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="preferences") 