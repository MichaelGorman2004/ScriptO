from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "ScriptO API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/scripto"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # AI Service settings
    AI_MODEL_PATH: str = "models/ai"
    RECOGNITION_THRESHOLD: float = 0.8

    class Config:
        env_file = ".env"

settings = Settings() 