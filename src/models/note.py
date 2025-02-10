from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class NoteElement(BaseModel):
    id: UUID
    type: str  # drawing, text, image, aiAnnotation
    content: dict
    bounds: dict
    timestamp: datetime
    stroke_properties: Optional[dict] = None

class Note(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: List[NoteElement]
    created: datetime
    modified: datetime
    tags: List[str]
    subject: Optional[str] = None 