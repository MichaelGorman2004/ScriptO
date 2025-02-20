from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from enum import Enum

from ..schemas.note_schema import NoteCreate, NoteResponse, NoteUpdate, NoteElement
from ..services.note_service import NoteService
from ..utils.response import APIResponse
from ..utils.logging import logger
from ..middleware.rate_limiter import RateLimiter
from ..middleware.auth import get_current_user
from ..db.database import get_db_session

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=60)
note_service = NoteService()

# Define sort options
class NoteSortField(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    TITLE = "title"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

@router.post("/", response_model=APIResponse)
async def create_note(
    note: NoteCreate,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Create a new note"""
    try:
        logger.info(f"Creating note for user {current_user_id}")
        created_note = await note_service.create_note(db, note, current_user_id)
        
        return APIResponse(
            success=True,
            message="Note created successfully",
            data=created_note,
            metadata={
                "timestamp": datetime.now(UTC),
                "note_id": str(created_note.id)
            }
        )
    except Exception as e:
        logger.error(f"Error creating note: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create note")

@router.get("/{note_id}", response_model=APIResponse)
async def get_note(
    note_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Get a specific note"""
    try:
        note = await note_service.get_note(db, note_id, current_user_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
            
        return APIResponse(
            success=True,
            message="Note retrieved successfully",
            data=note
        )
    except Exception as e:
        logger.error(f"Error retrieving note: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve note")

@router.put("/{note_id}", response_model=APIResponse)
async def update_note(
    note_id: UUID,
    note: NoteUpdate,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Update an existing note"""
    try:
        updated_note = await note_service.update_note(db, note_id, note, current_user_id)
        if not updated_note:
            raise HTTPException(status_code=404, detail="Note not found")
            
        return APIResponse(
            success=True,
            message="Note updated successfully",
            data=updated_note
        )
    except Exception as e:
        logger.error(f"Error updating note: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update note")

@router.delete("/{note_id}", response_model=APIResponse)
async def delete_note(
    note_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Delete a note"""
    try:
        success = await note_service.delete_note(db, note_id, current_user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Note not found")
            
        return APIResponse(
            success=True,
            message="Note deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting note: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete note")

@router.get("/", response_model=APIResponse)
async def list_notes(
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """List all notes for a user"""
    try:
        notes = await note_service.get_user_notes(db, current_user_id, skip, limit)
        return APIResponse(
            success=True,
            message="Notes retrieved successfully",
            data=notes,
            metadata={
                "total": len(notes),
                "skip": skip,
                "limit": limit
            }
        )
    except Exception as e:
        logger.error(f"Error listing notes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list notes")

@router.post("/{note_id}/elements", response_model=APIResponse)
async def add_element(
    note_id: UUID,
    element: NoteElement,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Add an element to a note"""
    try:
        updated_note = await note_service.add_element(db, note_id, element, current_user_id)
        if not updated_note:
            raise HTTPException(status_code=404, detail="Note not found")
            
        return APIResponse(
            success=True,
            message="Element added successfully",
            data=updated_note
        )
    except Exception as e:
        logger.error(f"Error adding element: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add element")

@router.post("/share/{note_id}")
async def share_note(note_id: UUID, user_ids: List[UUID]):
    return await NoteService.share_note(note_id, user_ids)

@router.get("/search", response_model=APIResponse)
async def search_notes(
    query: str,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session),
    sort_by: str = "modified",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 100
):
    """
    Search through user's notes with sorting options
    
    TODO: Future improvements
    - Add pagination metadata
    - Add cursor-based pagination
    - Add relevance scoring
    - Add faceted search
    """
    try:
        notes = await note_service.search_notes(
            db=db,
            user_id=current_user_id,
            query=query,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit
        )
        
        return APIResponse(
            success=True,
            message="Search completed successfully",
            data=notes,
            metadata={
                "total": len(notes),
                "query": query,
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        )
    except Exception as e:
        logger.error(f"Error searching notes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search notes")

@router.delete("/bulk", response_model=APIResponse)
async def bulk_delete_notes(
    note_ids: List[UUID],
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Delete multiple notes at once"""
    try:
        deleted_count = await note_service.bulk_delete_notes(db, note_ids, current_user_id)
        
        return APIResponse(
            success=True,
            message=f"Successfully deleted {deleted_count} notes",
            metadata={
                "deleted_count": deleted_count,
                "total_requested": len(note_ids)
            }
        )
    except Exception as e:
        logger.error(f"Error in bulk delete: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete notes")

"""
TODO: Future Improvements

1. Pagination:
   - Implement cursor-based pagination for better performance
   - Add total count caching
   - Add page info in response metadata

2. Element Operations:
   - Add bulk element operations
   - Add element reordering
   - Add element versioning
   - Add element-specific search

3. Note Organization:
   - Add folders/categories
   - Add tags management
   - Add favorites/pinning
   - Add archiving

4. Collaboration:
   - Add real-time collaboration
   - Add comment system
   - Add change tracking
   - Add user permissions

5. Performance:
   - Add response caching
   - Add query optimization
   - Add batch processing
""" 