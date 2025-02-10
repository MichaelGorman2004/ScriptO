from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    content: str
    type: str
    context: Optional[str] = None

class SolutionRequest(BaseModel):
    problem: str
    subject: str
    context: Optional[str] = None

class AISuggestion(BaseModel):
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