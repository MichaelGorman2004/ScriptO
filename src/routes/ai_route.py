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
from ..db.database import get_db_session
from ..utils.logging import logger

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=30)
ai_service = AIService()

@router.post("/solve", response_model=APIResponse)
async def solve_stem_problem(
    request: StemProblemRequest,
    background_tasks: BackgroundTasks,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Solve a STEM problem using AI
    
    This endpoint queues the problem for solving and returns immediately.
    The solution will be stored and can be retrieved later.
    Rate limited to 30 requests per minute per user.
    """
    try:
        logger.info(f"STEM problem solving request received for user {current_user_id}")
        await rate_limiter(request)
        
        # Create a pending interaction record
        interaction_id = await ai_service.create_pending_interaction(
            db=db,
            user_id=current_user_id,
            interaction_type="stem_solution",
            request_data={
                "problem": request.problem,
                "subject": request.subject,
                "context": request.context
            }
        )
        
        # Queue the actual processing
        background_tasks.add_task(
            ai_service.process_stem_problem,
            db=db,
            interaction_id=interaction_id,
            problem=request.problem,
            subject=request.subject,
            user_id=current_user_id,
            context=request.context
        )
        
        return APIResponse(
            success=True,
            message="Problem solving queued successfully",
            metadata={
                "timestamp": datetime.now(UTC),
                "interaction_id": str(interaction_id),
                "status": "processing"
            }
        )
        
    except Exception as e:
        logger.error(f"Error queueing stem problem: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to queue problem")

@router.post("/define", response_model=APIResponse)
async def define_term(
    request: DefinitionRequest,
    background_tasks: BackgroundTasks,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Define and explain a term using AI
    
    This endpoint queues the term for definition and returns immediately.
    The definition will be stored and can be retrieved later.
    Rate limited to 30 requests per minute per user.
    """
    try:
        logger.info(f"Term definition request received for user {current_user_id}")
        await rate_limiter(request)
        
        # Create a pending interaction record
        interaction_id = await ai_service.create_pending_interaction(
            db=db,
            user_id=current_user_id,
            interaction_type="term_definition",
            request_data={
                "term": request.term,
                "context": request.context
            }
        )
        
        # Queue the actual processing
        background_tasks.add_task(
            ai_service.process_term_definition,
            db=db,
            interaction_id=interaction_id,
            term=request.term,
            user_id=current_user_id,
            context=request.context
        )
        
        return APIResponse(
            success=True,
            message="Term definition queued successfully",
            metadata={
                "timestamp": datetime.now(UTC),
                "interaction_id": str(interaction_id),
                "status": "processing"
            }
        )
        
    except Exception as e:
        logger.error(f"Error queueing term definition: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to queue definition")

@router.get("/status/{interaction_id}", response_model=APIResponse)
async def check_status(
    interaction_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """Check the status of an AI interaction"""
    try:
        interaction = await ai_service.get_interaction(db, interaction_id, current_user_id)
        if not interaction:
            raise HTTPException(status_code=404, detail="Interaction not found")
            
        return APIResponse(
            success=True,
            message="Status retrieved successfully",
            data=interaction.response_data if interaction.response_data else None,
            metadata={
                "status": interaction.status,
                "created_at": interaction.created_at,
                "completed_at": interaction.completed_at
            }
        )
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check status")

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