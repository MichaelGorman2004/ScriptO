from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class NoteElementBase(BaseModel):
    type: str
    content: dict
    bounds: dict
    stroke_properties: Optional[dict] = None

class NoteElement(NoteElementBase):
    id: UUID
    note_id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: str
    tags: List[str]
    subject: Optional[str] = None

class NoteCreate(NoteBase):
    content: List[NoteElementBase]

class NoteUpdate(NoteBase):
    content: Optional[List[NoteElementBase]] = None

class NoteResponse(NoteBase):
    id: UUID
    user_id: UUID
    content: List[NoteElement]
    created: datetime
    modified: datetime

    class Config:
        from_attributes = True 