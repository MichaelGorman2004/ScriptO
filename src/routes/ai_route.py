from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from ..schemas.ai_schema import StemProblemRequest, DefinitionRequest, AIResponse
from ..services.ai_service import AIService
from ..utils.response import APIResponse
from ..middleware.rate_limiter import RateLimiter
from ..middleware.auth import get_current_user
from ..db.database import get_db
from ..utils.logging import logger

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=30)
ai_service = AIService()

@router.post("/solve", response_model=APIResponse)
async def solve_stem_problem(
    request: StemProblemRequest,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Solve a STEM problem using AI
    
    This endpoint processes and solves STEM problems using Claude AI.
    Rate limited to 30 requests per minute per user.
    """
    try:
        logger.info(f"STEM problem solving request received for user {current_user_id}")
        await rate_limiter(request)
        
        solution = await ai_service.solve_stem_problem(
            db=db,
            problem=request.problem,
            subject=request.subject,
            user_id=current_user_id
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
        
    except Exception as e:
        logger.error(f"Error in solve_stem_problem: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/define", response_model=APIResponse)
async def define_term(
    request: DefinitionRequest,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Define and explain a term using AI
    
    This endpoint provides comprehensive definitions and explanations using Claude AI.
    Rate limited to 30 requests per minute per user.
    """
    try:
        logger.info(f"Term definition request received for user {current_user_id}")
        await rate_limiter(request)
        
        definition = await ai_service.define_term(
            db=db,
            term=request.term,
            context=request.context,
            user_id=current_user_id
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
        
    except Exception as e:
        logger.error(f"Error in define_term: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

"""
TODO: Future Improvements

1. Response Caching:
   - Add caching for common STEM problems
   - Add caching for frequently requested definitions
   - Implement cache invalidation strategy

2. Request Queuing:
   - Add proper job queue for long-running requests
   - Add progress tracking
   - Add webhook notifications

3. AI Optimization:
   - Add request batching
   - Add response streaming
   - Add context management

4. Error Handling:
   - Add retry strategies
   - Add fallback providers
   - Add error classification

5. Monitoring:
   - Add performance metrics
   - Add usage tracking
   - Add cost monitoring
"""