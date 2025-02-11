"""
AI Service Module

This module handles AI-related operations:
1. STEM problem solving
2. Term definitions
"""

from typing import Dict, Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..schemas.ai_schema import AIResponse
from ..models.ai_model import AIInteraction
from .base_service import BaseService
from ..ai.providers.claude_provider import ClaudeProvider
from ..ai.processors.problem_processor import ProblemProcessor
from ..ai.processors.content_processor import ContentProcessor
from ..ai.config.ai_config import AIConfig
from ..ai.utils.exceptions import AIError, ProcessingError

class AIService(BaseService[AIInteraction, AIResponse, AIResponse]):
    """Service for handling AI-related operations."""
    
    def __init__(self, db: Session, api_key: str, config: Optional[AIConfig] = None):
        super().__init__(model=AIInteraction, db=db)
        self.config = config or AIConfig()
        self.provider = ClaudeProvider(api_key=api_key)
        self.problem_processor = ProblemProcessor(ai_provider=self.provider)
        self.content_processor = ContentProcessor(ai_provider=self.provider)
    
    async def solve_stem_problem(self, problem: str, user_id: UUID, context: Dict = None) -> AIResponse:
        """
        Process and solve a STEM problem
        
        Args:
            problem: The STEM problem to solve
            user_id: UUID of the requesting user
            context: Optional context like subject, grade level
            
        Returns:
            AIResponse containing the solution
            
        Raises:
            HTTPException: If processing or solution generation fails
        """
        try:
            # Process the problem
            processed = await self.problem_processor.process(problem, context)
            
            # Generate solution
            solution = await self.provider.solve_stem_problem(
                problem=processed["processed_text"],
                subject=processed["subject"]
            )
            
            # Create response
            response = AIResponse(
                id=UUID(),
                type="stem_solution",
                content=solution["solution"],
                subject=solution["subject"]
            )
            
            # Log interaction
            await self._log_interaction(
                user_id=user_id,
                request_data={"problem": problem, "context": context},
                response=response
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to solve STEM problem: {str(e)}"
            )
    
    async def define_term(self, term: str, user_id: UUID, context: Dict = None) -> AIResponse:
        """
        Process and define a term
        
        Args:
            term: The term to define
            user_id: UUID of the requesting user
            context: Optional context like subject, grade level
            
        Returns:
            AIResponse containing the definition
            
        Raises:
            HTTPException: If processing or definition generation fails
        """
        try:
            # Process the term
            processed = await self.content_processor.process(term, context)
            
            # Generate definition
            definition = await self.provider.define_term(
                term=processed["processed_term"],
                context=processed
            )
            
            # Create response
            response = AIResponse(
                id=UUID(),
                type="term_definition",
                content=definition["definition"],
                subject=definition["context"].get("subject", "general")
            )
            
            # Log interaction
            await self._log_interaction(
                user_id=user_id,
                request_data={"term": term, "context": context},
                response=response
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to define term: {str(e)}"
            )
    
    async def _log_interaction(
        self,
        user_id: UUID,
        request_data: Dict,
        response: AIResponse
    ) -> None:
        """Log AI interaction for tracking."""
        interaction = AIInteraction(
            user_id=user_id,
            request_data=request_data,
            response_data=response.model_dump(),
            created_at=datetime.utcnow()
        )
        self.db.add(interaction)
        self.db.commit() 