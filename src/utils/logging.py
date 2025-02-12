import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging() -> logging.Logger:
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("scripto")
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/scripto.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 