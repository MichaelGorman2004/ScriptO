from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict
from uuid import UUID
import logging
from datetime import datetime, UTC

from ..schemas.ai_schema import StemProblemRequest, DefinitionRequest, AIResponse
from ..services.ai_service import AIService
from ..utils.response import APIResponse
from ..middleware.rate_limiter import RateLimiter
from ..utils.logging import logger
from ..ai.providers.claude_provider import ClaudeProvider
from ..ai.config.ai_config import AIConfig

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=30)

# Initialize AI provider
ai_config = AIConfig()
claude_provider = ClaudeProvider(config=ai_config)

@router.post("/solve", response_model=APIResponse)
async def solve_stem_problem(
    request: StemProblemRequest,
    background_tasks: BackgroundTasks,
    user_id: UUID  # Will come from JWT auth later
):
    """
    Solve a STEM problem using AI
    
    This endpoint processes and solves STEM problems using Claude AI.
    Rate limited to 30 requests per minute per user.
    """
    try:
        logger.info(f"STEM problem solving request received for user {user_id}")
        await rate_limiter(request)
        
        # Queue the solution task
        solution = await claude_provider.solve_stem_problem(
            problem=request.problem,
            subject=request.subject
        )
        
        return APIResponse(
            success=True,
            message="Problem solved successfully",
            data=solution,
            metadata={
                "timestamp": datetime.now(UTC),
                "request_id": str(UUID()),
                "subject": request.subject
            }
        )
        
    except HTTPException as e:
        logger.error(f"HTTP error in solve_stem_problem: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in solve_stem_problem: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/define", response_model=APIResponse)
async def define_term(
    request: DefinitionRequest,
    background_tasks: BackgroundTasks,
    user_id: UUID  # Will come from JWT auth later
):
    """
    Define and explain a term using AI
    
    This endpoint provides comprehensive definitions and explanations using Claude AI.
    Rate limited to 30 requests per minute per user.
    """
    try:
        logger.info(f"Term definition request received for user {user_id}")
        await rate_limiter(request)
        
        # Get definition from Claude
        definition = await claude_provider.define_term(
            term=request.term,
            context=request.context
        )
        
        return APIResponse(
            success=True,
            message="Term defined successfully",
            data=definition,
            metadata={
                "timestamp": datetime.now(UTC),
                "request_id": str(UUID()),
                "term": request.term
            }
        )
        
    except HTTPException as e:
        logger.error(f"HTTP error in define_term: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in define_term: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")