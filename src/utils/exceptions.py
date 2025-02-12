class AIError(Exception):
    """Base exception for AI-related errors"""
    pass

class DatabaseError(Exception):
    """Base exception for database-related errors"""
    pass

class AuthenticationError(Exception):
    """Base exception for authentication-related errors"""
    pass 