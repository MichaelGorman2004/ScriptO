from typing import Optional, Any, Dict
from datetime import datetime, UTC
from pydantic import BaseModel

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    message: str
    data: Optional[Any] = None
    metadata: Dict = {
        "timestamp": datetime.now(UTC),
        "version": "1.0"
    } 