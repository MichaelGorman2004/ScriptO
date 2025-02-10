from typing import Dict, Any
import re
from .processor_base import ProcessorBase

class ProblemProcessor(ProcessorBase):
    """Preprocesses STEM problems before sending to AI"""
    
    async def process(self, content: str, context: Dict = None) -> Dict[str, Any]:
        """Main entry point for processing STEM problems"""
        context = context or {}
        subject = await self._detect_subject(content, context.get('subject'))
        return await self.process_problem(content, subject)
    
    async def process_problem(self, problem: str, subject: str) -> Dict:
        """
        Preprocesses a STEM problem by:
        1. Cleaning and formatting the text
        2. Identifying mathematical expressions for LaTeX formatting
        """
        cleaned_problem = self._clean_text(problem)
        cleaned_problem = self._normalize_math_symbols(cleaned_problem)
        
        math_parts = self._extract_math_expressions(cleaned_problem)
        
        return {
            "processed_text": cleaned_problem,
            "math_expressions": math_parts,
            "subject": subject,
            "has_equations": bool(math_parts)
        }
    
    def _normalize_math_symbols(self, text: str) -> str:
        """Normalizes mathematical symbols"""
        replacements = {
            '×': '*',
            '÷': '/',
            '−': '-',
            '=': ' = ',
            '+': ' + ',
            '-': ' - ',
            '*': ' * ',
            '/': ' / '
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def _extract_math_expressions(self, text: str) -> list:
        """
        Identifies and extracts mathematical expressions for LaTeX formatting
        Returns a list of found mathematical expressions
        """
        patterns = [
            r'(?:\d+\.?\d*|\.\d+)\s*[-+*/=]\s*(?:\d+\.?\d*|\.\d+)',  # Basic arithmetic
            r'[a-zA-Z]\s*[-+*/=]\s*\d+',  # Variable operations
            r'[a-zA-Z]\([a-zA-Z]\)',  # Function notation
            r'\b\w+\s*=\s*[-+]?\d*\.?\d+',  # Assignments
            r'√\d+',  # Square roots
            r'\b[xyz]\b',  # Common variables
            r'\b[abc]\b',  # Common coefficients
            r'\(\s*[-+]?\d*\.?\d+\s*[,\s]\s*[-+]?\d*\.?\d+\s*\)',  # Coordinates
        ]
        
        math_expressions = []
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                expr = match.group().strip()
                if expr not in math_expressions:
                    math_expressions.append(expr)
        
        return math_expressions
