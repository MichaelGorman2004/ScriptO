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

from typing import List, Optional, Dict
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, String
from datetime import datetime, UTC

from src.models.note_model import Note, NoteElement
from src.schemas.note_schema import NoteCreate, NoteUpdate
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
    
    async def add_element(self, note_id: UUID, element: NoteElement, user_id: UUID) -> Optional[Note]:
        """
        Add an element to a note, ensuring user ownership
        
        Args:
            note_id: UUID of the note
            element: Element to add
            user_id: UUID of the user
            
        Returns:
            Updated note if successful, None if not found
        """
        note = await self.get_note(note_id, user_id)
        if not note:
            return None
            
        try:
            note.content.append(element.model_dump())
            note.modified = datetime.now(UTC)
            self.db.commit()
            self.db.refresh(note)
            return note
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error adding element: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to add element")
    
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
    
    async def search_notes(
        self,
        user_id: UUID,
        query: str,
        sort_by: str = "modified",
        sort_order: str = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Note]:
        """
        Search through user's notes with sorting options
        
        Args:
            user_id: UUID of the note owner
            query: Search query string
            sort_by: Field to sort by (created, modified, title)
            sort_order: Sort direction (asc, desc)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching notes
        """
        try:
            # Build base query
            query_obj = self.db.query(Note).filter(Note.user_id == user_id)
            
            # Add search conditions
            search_filter = or_(
                Note.title.ilike(f"%{query}%"),
                Note.content.cast(String).ilike(f"%{query}%"),
                Note.tags.cast(String).ilike(f"%{query}%")
            )
            query_obj = query_obj.filter(search_filter)
            
            # Add sorting
            sort_column = getattr(Note, sort_by)
            if sort_order == "desc":
                query_obj = query_obj.order_by(desc(sort_column))
            else:
                query_obj = query_obj.order_by(asc(sort_column))
            
            # Add pagination
            return query_obj.offset(skip).limit(limit).all()
            
        except Exception as e:
            self.logger.error(f"Error in search_notes: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error during search")

    async def bulk_delete_notes(
        self,
        note_ids: List[UUID],
        user_id: UUID
    ) -> int:
        """
        Delete multiple notes at once
        
        Args:
            note_ids: List of note UUIDs to delete
            user_id: UUID of the note owner
            
        Returns:
            Number of notes successfully deleted
        """
        try:
            # Verify ownership and delete notes
            result = self.db.query(Note).filter(
                Note.id.in_(note_ids),
                Note.user_id == user_id
            ).delete(synchronize_session=False)
            
            self.db.commit()
            return result
            
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error in bulk_delete_notes: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete notes")

    async def get_note(self, note_id: UUID, user_id: UUID) -> Optional[Note]:
        """
        Get a specific note, ensuring user ownership
        
        Args:
            note_id: UUID of the note
            user_id: UUID of the user
            
        Returns:
            Note if found and owned by user, None otherwise
        """
        return self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()

    async def update_note(
        self,
        note_id: UUID,
        note_update: NoteUpdate,
        user_id: UUID
    ) -> Optional[Note]:
        """
        Update a note, ensuring user ownership
        
        Args:
            note_id: UUID of the note to update
            note_update: Update data
            user_id: UUID of the user
            
        Returns:
            Updated note if successful, None if not found
        """
        note = await self.get_note(note_id, user_id)
        if not note:
            return None
            
        update_data = note_update.model_dump(exclude_unset=True)
        update_data["modified"] = datetime.now(UTC)
        
        for field, value in update_data.items():
            setattr(note, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(note)
            return note
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error updating note: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update note") 