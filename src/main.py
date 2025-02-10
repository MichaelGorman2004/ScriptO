from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.router import api_router  # Updated import path

app = FastAPI(
    title="ScriptO API",
    description="Backend API for ScriptO note-taking and AI assistance platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main API router
app.include_router(api_router, prefix="/api/v1") 