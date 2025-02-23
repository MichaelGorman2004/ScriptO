from fastapi import Request, HTTPException
from typing import Dict, Tuple
from datetime import datetime, timedelta, UTC
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}

    async def __call__(self, request: Request):
        client_ip = request.client.host
        now = datetime.now()

        # Initialize or clean old requests
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if now - req_time < timedelta(minutes=1)
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429, 
                detail="Too many requests. Please try again later."
            )

        # Add new request
        self.requests[client_ip].append(now)

class DrawingRateLimiter(RateLimiter):
    def __init__(self, points_per_minute: int = 100000):
        super().__init__(requests_per_minute=30)
        self.points_per_minute = points_per_minute
        self.points_counter = 0
        self.last_reset = datetime.now(UTC)
    
    async def check_rate_limit(self, request: Request):
        # Reset counter if minute has passed
        now = datetime.now(UTC)
        if (now - self.last_reset).seconds >= 60:
            self.points_counter = 0
            self.last_reset = now
        
        # Check content size
        if request.headers.get("content-length"):
            size = int(request.headers["content-length"])
            if size > 1_000_000:  # 1MB limit
                raise HTTPException(
                    status_code=413,
                    detail="Request too large"
                )
        
        return await super().check_rate_limit(request) 