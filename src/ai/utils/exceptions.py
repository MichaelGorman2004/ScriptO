class AIError(Exception):
    """Base exception for AI-related errors"""
    pass

class AIProviderError(AIError):
    """Errors from the AI provider"""
    pass

class ProcessingError(AIError):
    """Errors during content processing"""
    pass

class ConfigurationError(AIError):
    """Errors in configuration"""
    pass 