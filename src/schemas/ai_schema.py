"""
AI Schema Definitions for the API

This module defines the Pydantic models for AI-related functionality,
"""

from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field

class StemProblemRequest(BaseModel):
    """Request schema for STEM problem solving"""
    problem: str = Field(..., min_length=1, max_length=2000)
    subject: str = Field(..., min_length=1, max_length=50)
    context: Optional[Dict] = None

class DefinitionRequest(BaseModel):
    """Request schema for term definitions"""
    term: str = Field(..., min_length=1, max_length=100)
    context: Optional[Dict] = None

class AIResponse(BaseModel):
    """Response schema for AI-generated content"""
    id: UUID
    type: str = Field(..., pattern="^(stem_solution|term_definition)$")
    content: str
    subject: str
    confidence: float = Field(..., ge=0.0, le=1.0)

    class Config:
        from_attributes = True 