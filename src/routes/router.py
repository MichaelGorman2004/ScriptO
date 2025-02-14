from fastapi import APIRouter
from .note_route import router as notes_router
from .ai_route import router as ai_router
from .user_route import router as users_router
from .auth_route import router as auth_router

# Main API Router
api_router = APIRouter()

# Include auth routes first (these don't need auth middleware)
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"]
)

# Include all other route modules (these will need auth middleware)
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