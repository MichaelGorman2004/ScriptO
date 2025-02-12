"""
Note Service Module

This module handles all note-related operations including note management,
element handling, and note organization.

Key Features:
- Note CRUD operations
- Note element management
- Version tracking
- Note organization and metadata handling
"""

from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from src.models.note_model import Note
from src.schemas.note_schema import NoteCreate, NoteUpdate, NoteElement
from src.services.base_service import BaseService

class NoteService(BaseService[Note, NoteCreate, NoteUpdate]):
    """
    Service for handling note-related operations.
    
    Extends the BaseService with note-specific functionality including
    element management and version control.
    """
    
    def __init__(self, db: Session):
        super().__init__(model=Note, db=db)
    
    async def create_note(self, note_create: NoteCreate, user_id: UUID) -> Note:
        """
        Create a new note with associated user.
        
        Args:
            note_create: NoteCreate schema containing note data
            user_id: UUID of the note owner
            
        Returns:
            Created note instance
        """
        note_data = note_create.model_dump()
        note_data["user_id"] = user_id
        note_data["created_at"] = datetime.now(UTC)
        note_data["updated_at"] = datetime.now(UTC)
        
        return await super().create(NoteCreate(**note_data))
    
    async def add_element(self, note_id: UUID, element: NoteElement) -> Note:
        """
        Add a new element to an existing note.
        
        Args:
            note_id: UUID of the note
            element: NoteElement schema containing element data
            
        Returns:
            Updated note instance
            
        Raises:
            HTTPException: If note not found
        """
        note = await self.get(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        note.elements.append(element.model_dump())
        note.updated_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    async def update_element(self, note_id: UUID, element_id: UUID, element: NoteElement) -> Note:
        """
        Update an existing element in a note.
        
        Args:
            note_id: UUID of the note
            element_id: UUID of the element to update
            element: Updated element data
            
        Returns:
            Updated note instance
            
        Raises:
            HTTPException: If note or element not found
        """
        note = await self.get(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        element_found = False
        for idx, existing_element in enumerate(note.elements):
            if existing_element.get("id") == str(element_id):
                note.elements[idx] = element.model_dump()
                element_found = True
                break
                
        if not element_found:
            raise HTTPException(status_code=404, detail="Element not found")
        
        note.updated_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    async def remove_element(self, note_id: UUID, element_id: UUID) -> Note:
        """
        Remove an element from a note.
        
        Args:
            note_id: UUID of the note
            element_id: UUID of the element to remove
            
        Returns:
            Updated note instance
            
        Raises:
            HTTPException: If note or element not found
        """
        note = await self.get(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        original_length = len(note.elements)
        note.elements = [e for e in note.elements if e.get("id") != str(element_id)]
        
        if len(note.elements) == original_length:
            raise HTTPException(status_code=404, detail="Element not found")
        
        note.updated_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    async def get_user_notes(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Note]:
        """
        Retrieve all notes for a specific user.
        
        Args:
            user_id: UUID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of notes
        """
        return (self.db.query(self.model)
                .filter(self.model.user_id == user_id)
                .offset(skip)
                .limit(limit)
                .all())
    
    async def search_notes(self, user_id: UUID, query: str) -> List[Note]:
        """
        Search through user's notes.
        
        Args:
            user_id: UUID of the user
            query: Search query string
            
        Returns:
            List of matching notes
        """
        return (self.db.query(self.model)
                .filter(self.model.user_id == user_id)
                .filter(self.model.content.ilike(f"%{query}%"))
                .all()) 