from typing import Dict, List
import anthropic
from .base_provider import BaseAIProvider

class ClaudeProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.default_model = "claude-3-sonnet-20240229"
        
    async def generate_completion(self, prompt: str, parameters: dict) -> str:
        try:
            model = parameters.get("model", self.default_model)
            temperature = parameters.get("temperature", 0.7)
            max_tokens = parameters.get("max_tokens", 1500)
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
            # Log the error
            raise Exception(f"Claude completion failed: {str(e)}")
    
    async def solve_stem_problem(self, problem: str, subject: str) -> Dict:
        """
        Solves a STEM problem with detailed steps and explanations
        """
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

        <format>
        # Problem Analysis
        [Your analysis here]

        # Step-by-Step Solution
        1. [First step with explanation]
        2. [Second step with explanation]
        ...

        # Final Answer
        [Clear statement of the final answer]

        # Key Concepts Used
        - [Concept 1]
        - [Concept 2]
        </format>
        """

        response = await self.generate_completion(prompt, {
            "temperature": 0.3,
            "system": "You are an expert STEM tutor. Provide clear, detailed solutions with step-by-step explanations."
        })

        return {
            "solution": response,
            "subject": subject,
            "type": "stem_solution"
        }

    async def define_term(self, term: str, context: Dict = None) -> Dict:
        """
        Provides a comprehensive definition and explanation of a term
        """
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

        <format>
        # Definition
        [Clear, concise definition]

        # Detailed Explanation
        [More detailed explanation with context]

        # Examples
        1. [First example]
        2. [Second example]

        # Related Concepts
        - [Related concept 1]
        - [Related concept 2]

        # Usage in {subject}
        [How this term is used in the subject]
        </format>
        """

        response = await self.generate_completion(prompt, {
            "temperature": 0.3,
            "system": "You are an expert educator explaining concepts at an appropriate level."
        })

        return {
            "definition": response,
            "term": term,
            "context": context,
            "type": "term_definition"
        } 