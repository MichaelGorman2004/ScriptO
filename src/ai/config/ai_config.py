from typing import Dict
from dataclasses import dataclass

@dataclass
class AIConfig:
    """Configuration for AI services"""
    
    # Model selection
    default_model: str = "claude-3-sonnet-20240229"
    fallback_model: str = "claude-3-haiku-20240307"
    
    # Request parameters
    max_tokens: int = 1500
    default_temperature: float = 0.7
    stem_temperature: float = 0.3  # Lower temperature for STEM solutions
    definition_temperature: float = 0.3  # Lower temperature for definitions
    
    # Timeouts and retries
    request_timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'AIConfig':
        return cls(**{
            k: v for k, v in config_dict.items() 
            if k in cls.__dataclass_fields__
        }) 