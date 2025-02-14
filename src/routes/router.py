from fastapi import APIRouter
from .note_routes import router as notes_router
from .ai_routes import router as ai_router
from .user_routes import router as users_router

# Main API Router
api_router = APIRouter()

# Include all route modules
api_router.include_router(
    notes_router,
    prefix="/notes",
    tags=["notes"]
)

api_router.include_router(
    ai_router,
    prefix="/ai",
    tags=["ai"]
)

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
) 