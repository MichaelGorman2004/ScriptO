from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy import Column, DateTime, String, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from src.db.database import Base

class AIAssistant(Base):
    __tablename__ = "ai_assistants"

    id = Column(PGUUID, primary_key=True, index=True)
    type = Column(String)  # math, physics, chemistry, biology, vocabulary
    context = Column(String)
    confidence = Column(Float)
    suggestions = Column(JSON)  # Store suggestions as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    note_id = Column(PGUUID, ForeignKey("notes.id"))

    note = relationship("Note") 