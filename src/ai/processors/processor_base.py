from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..providers.claude_provider import ClaudeProvider

class ProcessorBase(ABC):
    """Base class for all content processors"""
    
    # Standard STEM subjects we support
    SUPPORTED_SUBJECTS = [
        "algebra",
        "geometry",
        "calculus",
        "physics",
        "chemistry",
        "biology",
        "statistics",
        "computer science",
        "general math"
    ]
    
    def __init__(self, ai_provider: ClaudeProvider = None):
        """Initialize with optional AI provider"""
        self.ai_provider = ai_provider
    
    def _clean_text(self, text: str) -> str:
        """
        Basic text cleaning shared by all processors
        - Removes extra whitespace
        - Normalizes basic characters
        """
        return " ".join(text.split())
    
    async def _detect_subject(self, text: str, provided_subject: str = None) -> str:
        """
        Detects the subject area using Claude if available, otherwise returns provided_subject or 'general'
        """
        if provided_subject and provided_subject.lower() in self.SUPPORTED_SUBJECTS:
            return provided_subject.lower()
            
        if self.ai_provider:
            prompt = f"""
            <content>
            {text}
            </content>

            <supported_subjects>
            {', '.join(self.SUPPORTED_SUBJECTS)}
            </supported_subjects>

            <instructions>
            Based on the content above, identify which subject from the supported_subjects list best matches.
            Consider:
            1. Key terms and concepts
            2. Type of problem or discussion
            3. Mathematical notation or scientific terminology

            Respond with ONLY the single best matching subject name from the list, in lowercase.
            If uncertain, respond with "general math".
            </instructions>
            """

            try:
                response = await self.ai_provider.generate_completion(prompt, {
                    "temperature": 0.1,  # Low temperature for consistent subject classification
                    "system": "You are a STEM subject classifier. Respond only with the subject name."
                })
                
                detected = response.strip().lower()
                if detected in self.SUPPORTED_SUBJECTS:
                    return detected
                    
            except Exception as e:
                # If AI detection fails, fall back to default
                pass
                
        return "general math"
    
    @abstractmethod
    def process(self, content: str, context: Dict = None) -> Dict[str, Any]:
        """Main processing method to be implemented by subclasses"""
        pass 