from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from ..schemas.note import NoteCreate, NoteResponse, NoteUpdate
from ..services.note_service import NoteService

router = APIRouter()

@router.post("/create", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    return await NoteService.create_note(note)

@router.put("/update/{note_id}", response_model=NoteResponse)
async def update_note(note_id: UUID, note: NoteUpdate):
    return await NoteService.update_note(note_id, note)

@router.post("/share/{note_id}")
async def share_note(note_id: UUID, user_ids: List[UUID]):
    return await NoteService.share_note(note_id, user_ids)

@router.get("/search", response_model=List[NoteResponse])
async def search_notes(query: str):
    return await NoteService.search_notes(query) 