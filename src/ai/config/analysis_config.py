from typing import Dict
from dataclasses import dataclass

@dataclass
class AnalysisConfig:
    """Configuration for content analysis"""
    
    # Model selection parameters
    default_model: str = "claude-3-sonnet-20240229"
    fallback_model: str = "claude-3-haiku-20240307"
    
    # Analysis parameters
    min_confidence_threshold: float = 0.7
    max_retries: int = 3
    timeout_seconds: int = 30
    
    # Processing parameters
    max_content_length: int = 8000
    chunk_size: int = 2000
    overlap_size: int = 200
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'AnalysisConfig':
        return cls(**{
            k: v for k, v in config_dict.items() 
            if k in cls.__dataclass_fields__
        }) 