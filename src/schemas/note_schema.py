"""
Note Schema Definitions for the API

This module defines the Pydantic models used for note-related data validation and serialization.
The schema supports a hierarchical structure where each note contains multiple note elements
(e.g., text blocks, drawings, images) with their respective properties.

Key Components:
- NoteElementBase: Base schema for individual elements within a note (e.g., text, drawings)
- NoteElement: Complete schema for note elements including metadata
- NoteBase: Common note properties shared across different note schemas
- NoteCreate: Schema for creating new notes
- NoteUpdate: Schema for updating existing notes
- NoteResponse: Schema for API responses containing complete note information
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class NoteElementBase(BaseModel):
    """
    Base schema for note elements defining core properties.
    
    Attributes:
        type (str): The type of element (e.g., 'text', 'drawing', 'image')
        content (dict): Element-specific content data
        bounds (dict): Position and size information of the element
        stroke_properties (Optional[dict]): Properties for drawn elements (color, width, etc.)
    """
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