# AI Integration Implementation Guide

## Overview
This document outlines the implemented AI capabilities, focusing on STEM problem solving and term definitions using Claude as our AI provider.

## Directory Structure
```
src/
└── ai/
    ├── processors/
    │   ├── __init__.py
    │   ├── processor_base.py     # Base processor with shared functionality
    │   ├── problem_processor.py  # STEM problem preprocessing
    │   └── content_processor.py  # Term/concept preprocessing
    ├── providers/
    │   ├── __init__.py
    │   ├── base_provider.py     # Base AI provider interface
    │   └── claude_provider.py   # Claude-specific implementation
    └── utils/
        └── __init__.py          # Reserved for future utilities
```

## Core Components

### 1. AI Providers

#### Base Provider Interface
```python
class BaseAIProvider(ABC):
    async def generate_completion(self, prompt: str, parameters: dict) -> str
    async def solve_stem_problem(self, problem: str, subject: str) -> Dict
    async def define_term(self, term: str, context: Dict = None) -> Dict
```

#### Claude Implementation
- API key management
- Async request handling
- Error handling
- Response formatting
- Model selection (Claude-3-Sonnet by default)
- Structured output using markdown
- LaTeX support for mathematical expressions

### 2. Content Processing

#### Base Processor
```python
class ProcessorBase(ABC):
    """Base class with shared preprocessing functionality"""
    
    SUPPORTED_SUBJECTS = [
        "algebra", "geometry", "calculus", "physics",
        "chemistry", "biology", "statistics",
        "computer science", "general math"
    ]
    
    def _clean_text(self, text: str) -> str
    async def _detect_subject(self, text: str, provided_subject: str = None) -> str
```

#### Problem Processing
```python
class ProblemProcessor(ProcessorBase):
    """STEM problem preprocessing"""
    
    async def process_problem(self, problem: str, subject: str) -> Dict:
        # Handles:
        # 1. Text cleaning
        # 2. Math symbol normalization
        # 3. Mathematical expression extraction
```

#### Term Processing
```python
class ContentProcessor(ProcessorBase):
    """Term/concept preprocessing"""
    
    async def process_term(self, term: str, context: Dict = None) -> Dict:
        # Handles:
        # 1. Text cleaning
        # 2. Subject detection
        # 3. Educational level context
```

## Integration Examples

### STEM Problem Solving
```python
from ai.providers.claude_provider import ClaudeProvider
from ai.processors.problem_processor import ProblemProcessor

# Initialize components
provider = ClaudeProvider(api_key="your-key")
processor = ProblemProcessor(ai_provider=provider)

# Process and solve a problem
processed = await processor.process(
    content="Solve for x: 2x + 3 = 7",
    context={"subject": "algebra"}
)

solution = await provider.solve_stem_problem(
    problem=processed["processed_text"],
    subject=processed["subject"]
)
```

### Term Definition
```python
from ai.processors.content_processor import ContentProcessor

# Initialize components
processor = ContentProcessor(ai_provider=provider)

# Process and define a term
processed = await processor.process(
    content="derivative",
    context={
        "grade_level": "11th grade",
        "subject": "calculus"
    }
)

definition = await provider.define_term(
    term=processed["processed_term"],
    context=processed
)
```

## Key Features

### 1. STEM Problem Solving
- Step-by-step solutions
- LaTeX formatting for mathematical expressions
- Problem analysis
- Key concepts identification
- Clear final answers

### 2. Term Definitions
- Grade-appropriate explanations
- Real-world examples
- Related concepts
- Subject-specific context
- Clear markdown formatting

### 3. Subject Detection
- AI-powered subject classification
- Support for multiple STEM subjects
- Fallback to provided subject or general math
- Consistent subject categorization

## Best Practices

1. **Error Handling**
   - Implement try-catch blocks for AI calls
   - Provide meaningful error messages
   - Use fallback subjects when detection fails

2. **Performance**
   - Use async operations for AI calls
   - Implement efficient text preprocessing
   - Normalize mathematical symbols

3. **Quality**
   - Clean and normalize input text
   - Structure prompts clearly
   - Use appropriate temperature settings
   - Format responses in markdown

## Next Steps

1. ✅ Set up AI directory structure
2. ✅ Implement base interfaces
3. ✅ Implement Claude provider
4. ✅ Create preprocessing pipeline
5. ✅ Implement STEM problem solving
6. ✅ Implement term definitions
7. Future Enhancements:
   - Add response caching
   - Implement rate limiting
   - Add monitoring and logging
   - Expand math expression detection
   - Add more subject-specific processing

