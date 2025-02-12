from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import Column, DateTime, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from src.db.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(PGUUID, primary_key=True, index=True)
    user_id = Column(PGUUID, ForeignKey("users.id"))
    title = Column(String)
    content = relationship("NoteElement", back_populates="note")
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(JSON)  # Store as JSON array
    subject = Column(String, nullable=True)

    user = relationship("User", back_populates="notes")

class NoteElement(Base):
    __tablename__ = "note_elements"

    id = Column(PGUUID, primary_key=True, index=True)
    note_id = Column(PGUUID, ForeignKey("notes.id"))
    type = Column(String)  # drawing, text, image, aiAnnotation
    content = Column(JSON)
    bounds = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    stroke_properties = Column(JSON, nullable=True)

    note = relationship("Note", back_populates="content") 