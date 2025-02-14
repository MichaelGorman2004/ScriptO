from datetime import datetime
from typing import Dict
from uuid import UUID
from sqlalchemy import Column, DateTime, String, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from src.db.database import Base

class AIInteraction(Base):
    """Model for tracking AI interactions"""
    __tablename__ = "ai_interactions"

    id = Column(PGUUID, primary_key=True, index=True)
    user_id = Column(PGUUID, ForeignKey("users.id"))
    type = Column(String)  # stem_solution or term_definition
    status = Column(String)  # pending, processing, completed, failed
    request_data = Column(JSON)
    response_data = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True) 