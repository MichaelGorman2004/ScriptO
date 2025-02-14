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
from datetime import datetime, UTC

from src.schemas.ai_schema import AIResponse
from src.models.ai_model import AIInteraction
from src.services.base_service import BaseService
from src.ai.providers.claude_provider import ClaudeProvider
from src.ai.config.ai_config import AIConfig
from src.utils.logging import logger

class AIService(BaseService[AIInteraction, AIResponse, AIResponse]):
    """Service for handling AI-related operations."""
    
    def __init__(self):
        super().__init__(model=AIInteraction)
        self.config = AIConfig()
        self.provider = ClaudeProvider(config=self.config)
    
    async def solve_stem_problem(
        self,
        db: Session,
        problem: str,
        subject: str,
        user_id: UUID,
        context: Dict = None
    ) -> Dict:
        """Solve a STEM problem and log interaction"""
        try:
            # Get solution from Claude
            solution = await self.provider.solve_stem_problem(
                problem=problem,
                subject=subject
            )
            
            # Log interaction
            await self._log_interaction(
                db=db,
                user_id=user_id,
                interaction_type="stem_solution",
                request_data={"problem": problem, "subject": subject, "context": context},
                response_data=solution
            )
            
            return solution
            
        except Exception as e:
            logger.error(f"Error in solve_stem_problem: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to solve problem")
    
    async def define_term(
        self,
        db: Session,
        term: str,
        user_id: UUID,
        context: Dict = None
    ) -> Dict:
        """Define a term and log interaction"""
        try:
            # Get definition from Claude
            definition = await self.provider.define_term(
                term=term,
                context=context
            )
            
            # Log interaction
            await self._log_interaction(
                db=db,
                user_id=user_id,
                interaction_type="term_definition",
                request_data={"term": term, "context": context},
                response_data=definition
            )
            
            return definition
            
        except Exception as e:
            logger.error(f"Error in define_term: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to define term")
    
    async def _log_interaction(
        self,
        db: Session,
        user_id: UUID,
        interaction_type: str,
        request_data: Dict,
        response_data: Dict
    ) -> None:
        """Log AI interaction for tracking"""
        try:
            interaction = AIInteraction(
                user_id=user_id,
                type=interaction_type,
                request_data=request_data,
                response_data=response_data,
                created_at=datetime.now(UTC)
            )
            db.add(interaction)
            db.commit()
            
        except Exception as e:
            logger.error(f"Failed to log interaction: {str(e)}")
            # Don't fail the request if logging fails
            db.rollback() 