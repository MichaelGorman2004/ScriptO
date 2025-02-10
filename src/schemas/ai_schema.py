"""
AI Schema Definitions for the API

This module defines the Pydantic models for AI-related functionality,
including analysis requests, solution requests, and AI-generated responses.

Key Components:
- AnalysisRequest: Schema for requesting AI analysis of content
- SolutionRequest: Schema for requesting AI-generated solutions
- AISuggestion: Schema for individual AI-generated suggestions
- AIResponse: Schema for complete AI response including multiple suggestions
"""

from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    """
    Schema for requesting AI analysis of content.
    
    Attributes:
        content (str): The content to be analyzed
        type (str): Type of analysis requested
        context (Optional[str]): Additional context for the analysis
    """
    content: str
    type: str
    context: Optional[str] = None

class SolutionRequest(BaseModel):
    """
    Schema for requesting AI-generated solutions.
    
    Attributes:
        problem (str): The problem statement or question
        subject (str): The subject area or domain
        context (Optional[str]): Additional context for the solution
    """
    problem: str
    subject: str
    context: Optional[str] = None

class AISuggestion(BaseModel):
    """
    Schema for individual AI-generated suggestions.
    
    Attributes:
        type (str): Type of suggestion
        content (str): The actual suggestion content
        confidence (float): Confidence score for the suggestion
    """
    type: str
    content: str
    confidence: float

class AIResponse(BaseModel):
    id: UUID
    type: str
    suggestions: List[AISuggestion]
    confidence: float
    context: str

    class Config:
        from_attributes = True 