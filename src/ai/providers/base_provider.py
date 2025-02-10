from typing import Dict, List
from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    """Base interface for AI providers"""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, parameters: dict) -> str:
        """Generate a raw completion from the AI provider"""
        pass
    
    @abstractmethod
    async def solve_stem_problem(self, problem: str, subject: str) -> Dict:
        """Solve a STEM problem with detailed steps and explanations"""
        pass
    
    @abstractmethod
    async def define_term(self, term: str, context: Dict = None) -> Dict:
        """Provide a comprehensive definition and explanation of a term"""
        pass 