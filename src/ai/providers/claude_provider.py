from typing import Dict
import anthropic
from .base_provider import BaseAIProvider
from ..config.ai_config import AIConfig
from ..utils.exceptions import AIProviderError
from src.config.settings import settings

class ClaudeProvider(BaseAIProvider):
    def __init__(self, config: AIConfig = None):
        self.config = config or AIConfig()
        try:
            self.client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
        except Exception as e:
            raise AIProviderError(f"Failed to initialize Claude client: {str(e)}")
        
    async def generate_completion(self, prompt: str, parameters: dict) -> str:
        try:
            model = parameters.get("model", self.config.default_model)
            temperature = parameters.get("temperature", self.config.default_temperature)
            max_tokens = parameters.get("max_tokens", self.config.max_tokens)
            system = parameters.get("system", "")
            
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content
            
        except Exception as e:
            raise AIProviderError(f"Claude completion failed: {str(e)}")
    
    async def solve_stem_problem(self, problem: str, subject: str) -> Dict:
        try:
            prompt = f"""
            <problem>
            {problem}
            </problem>

            <subject>{subject}</subject>

            <instructions>
            Please solve this {subject} problem. Provide:
            1. Initial problem analysis
            2. Step-by-step solution with explanations
            3. Final answer clearly marked
            4. Key concepts used
            
            Format your response in markdown, with:
            - Clear headings for each section
            - Mathematical expressions in LaTeX when needed
            - Numbered steps
            - Clear explanations for each step
            </instructions>
            """

            response = await self.generate_completion(prompt, {
                "temperature": self.config.stem_temperature,
                "system": "You are an expert STEM tutor. Provide clear, detailed solutions with step-by-step explanations."
            })

            return {
                "solution": response,
                "subject": subject,
                "type": "stem_solution"
            }
        except Exception as e:
            raise AIProviderError(f"Failed to solve STEM problem: {str(e)}")

    async def define_term(self, term: str, context: Dict = None) -> Dict:
        try:
            context = context or {}
            grade_level = context.get('grade_level', 'high school')
            subject = context.get('subject', 'general')

            prompt = f"""
            <term>{term}</term>

            <context>
            <grade_level>{grade_level}</grade_level>
            <subject>{subject}</subject>
            </context>

            <instructions>
            Please provide a comprehensive explanation of this term with:
            1. A clear, grade-appropriate definition
            2. Real-world examples and applications
            3. Related concepts
            4. Usage in the subject area
            
            Format your response in markdown with clear sections.
            </instructions>
            """

            response = await self.generate_completion(prompt, {
                "temperature": self.config.definition_temperature,
                "system": "You are an expert educator explaining concepts at an appropriate level."
            })

            return {
                "definition": response,
                "term": term,
                "context": context,
                "type": "term_definition"
            }
        except Exception as e:
            raise AIProviderError(f"Failed to define term: {str(e)}") 