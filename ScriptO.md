# ScriptO Technical Design Document

## System Overview
ScriptO is a web-based note-taking application that combines handwriting recognition with real-time AI assistance for STEM subjects.

## Core Technical Requirements

### Frontend Architecture
- **Framework**: React with TypeScript
  - *Rationale*: Strong type safety, excellent ecosystem support, and component reusability
- **Styling**: TailwindCSS
  - *Rationale*: Rapid prototyping capabilities, utility-first approach for consistent design
- **State Management**: React Context + hooks for MVP
  - *Rationale*: Adequate for initial scope, can be extended to Redux if complexity grows

### Backend Architecture
- **Framework**: FastAPI
  - *Rationale*: High performance, async support, automatic OpenAPI docs
- **Database**: PostgreSQL
  - *Rationale*: Robust ACID compliance, JSON support for flexible note storage
- **Caching**: Redis
  - *Rationale*: Fast in-memory caching for frequent computations and session management

## Core Components

### 1. Note-Taking Interface

#### Canvas Implementation Options

##### Option 1: Pure Canvas API
```typescript
class CanvasManager {
    private context: CanvasRenderingContext2D;
    private currentStroke: Stroke = [];
    
    constructor(canvas: HTMLCanvasElement) {
        this.context = canvas.getContext('2d');
        this.setupEventListeners();
    }
    
    private setupEventListeners() {
        this.canvas.addEventListener('pointerdown', this.startStroke);
        this.canvas.addEventListener('pointermove', this.updateStroke);
        this.canvas.addEventListener('pointerup', this.endStroke);
    }
}
```
**Pros:**
- Full control over rendering
- Better performance
- Smaller bundle size

**Cons:**
- More complex to implement
- Need to handle all edge cases
- More difficult to add features

##### Option 2: Fabric.js Integration
```typescript
class FabricCanvasManager {
    private canvas: fabric.Canvas;
    
    constructor(canvasElement: HTMLCanvasElement) {
        this.canvas = new fabric.Canvas(canvasElement);
        this.setupBrushes();
    }
    
    private setupBrushes() {
        this.canvas.freeDrawingBrush = new fabric.PencilBrush(this.canvas);
        this.canvas.isDrawingMode = true;
    }
}
```
**Pros:**
- Many features built-in
- Better touch support
- Easier object manipulation

**Cons:**
- Larger bundle size
- Less control over internals
- Potential performance overhead

##### Option 3: Custom WebGL Renderer
```typescript
class WebGLCanvasManager {
    private gl: WebGLRenderingContext;
    private strokeShader: WebGLProgram;
    
    constructor(canvas: HTMLCanvasElement) {
        this.gl = canvas.getContext('webgl');
        this.strokeShader = this.createShaderProgram();
    }
    
    private createShaderProgram() {
        // Implement WebGL shader setup
    }
}
```
**Pros:**
- Best performance
- Hardware acceleration
- Smooth rendering

**Cons:**
- Most complex to implement
- Steeper learning curve
- More difficult to debug

#### Stroke Data Structure Options

##### Option 1: Simple Array
```typescript
interface Point {
    x: number;
    y: number;
    pressure: number;
    timestamp: number;
}

type Stroke = Point[];
```
**Pros:**
- Simple to understand
- Easy to serialize
- Lower memory usage

**Cons:**
- Limited metadata
- Harder to modify
- Less flexible

##### Option 2: Rich Object Model
```typescript
interface StrokeProperties {
    color: string;
    width: number;
    opacity: number;
    tool: 'pen' | 'highlighter' | 'eraser';
}

interface Stroke {
    points: Point[];
    properties: StrokeProperties;
    id: string;
    layer: number;
    created: Date;
    modified: Date;
}
```
**Pros:**
- More metadata
- Better for editing
- More features possible

**Cons:**
- More complex
- Higher memory usage
- More serialization overhead

#### Page Management Approaches

##### Option 1: Single Canvas with Viewport
```typescript
class SingleCanvasManager {
    private viewport: {
        x: number;
        y: number;
        scale: number;
        page: number;
    };
    
    public navigateToPage(page: number) {
        this.viewport.page = page;
        this.viewport.y = page * this.pageHeight;
        this.render();
    }
}
```
**Pros:**
- Simpler implementation
- Better performance
- Easier continuous scrolling

**Cons:**
- Memory limitations
- More complex zooming
- Page boundaries less clear

##### Option 2: Multiple Canvas Elements
```typescript
class MultiCanvasManager {
    private pages: Map<number, HTMLCanvasElement>;
    
    public addPage() {
        const canvas = document.createElement('canvas');
        const page = new CanvasManager(canvas);
        this.pages.set(this.pages.size, page);
    }
}
```
**Pros:**
- Clear page separation
- Better memory management
- Easier per-page operations

**Cons:**
- More DOM elements
- Harder continuous scrolling
- More complex synchronization
  
- **Assistant Integration**:
  ```typescript
  interface AssistantUI {
    // Right sidebar for solutions
    solutionPanel: {
      show(): void;
      hide(): void;
      updateContent(solution: StepByStepSolution): void;
    };
    
    // Inline definition completion
    definitionOverlay: {
      showSuggestion(completion: string): void;
      acceptSuggestion(): void;
      dismiss(): void;
    };
    
    // Note reorganization
    reorganizeButton: {
      position: 'top-right';
      onClick(): Promise<void>;
    };
  }
  ```

### 2. Canvas System
- HTML5 Canvas for drawing
- WebAssembly for performance-critical operations
- Real-time stroke smoothing and rendering
- Event system for gesture recognition

### 2. Recognition Pipeline
- **Handwriting Recognition**:
  ```python
  class RecognitionPipeline:
      async def process_stroke(self, points: List[Point]) -> RecognizedText:
          # 1. Normalize stroke data
          # 2. Run through OCR
          # 3. Return recognized text
  ```
- Integration with MyScript API for initial MVP
  - Fallback to Tesseract for offline capabilities

### 3. AI Assistant Integration

#### Architecture Alternatives

##### Option 1: Direct Integration
```python
class DirectClaudeAssistant:
    def __init__(self):
        self.client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
        
    async def process_request(self, content: str, task_type: str) -> Any:
        """Direct communication with Claude API."""
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            system=SYSTEM_PROMPTS[task_type],
            messages=[{"role": "user", "content": content}]
        )
        return self._parse_response(response, task_type)
```
**Pros:**
- Simple implementation
- Lower latency
- Easier to debug

**Cons:**
- Less flexible for complex workflows
- No caching layer
- Higher API costs

##### Option 2: Queue-Based Architecture
```python
class QueuedClaudeAssistant:
    def __init__(self):
        self.client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
        self.redis_client = Redis()
        self.task_queue = Queue()
        
    async def enqueue_request(self, content: str, task_type: str) -> str:
        """Queue request for processing."""
        task_id = str(uuid.uuid4())
        await self.task_queue.put({
            'id': task_id,
            'content': content,
            'type': task_type,
            'status': 'pending'
        })
        return task_id
        
    async def process_queue(self):
        """Background worker processing queued requests."""
        while True:
            task = await self.task_queue.get()
            result = await self._process_task(task)
            await self.redis_client.set(f"result:{task['id']}", result)
```
**Pros:**
- Better handling of concurrent requests
- Ability to implement retry logic
- Easier to scale
- Can implement caching

**Cons:**
- More complex architecture
- Higher latency
- More infrastructure needed

##### Option 3: Streaming Architecture
```python
class StreamingClaudeAssistant:
    def __init__(self):
        self.client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
        
    async def stream_solution(self, content: str) -> AsyncGenerator:
        """Stream solution steps as they're generated."""
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            system=SYSTEM_PROMPTS['problem_solving'],
            messages=[{"role": "user", "content": content}],
            stream=True
        )
        
        async for chunk in response:
            yield self._parse_chunk(chunk)
```
**Pros:**
- Better user experience for long responses
- Lower perceived latency
- More interactive feel

**Cons:**
- More complex frontend integration
- Harder to implement caching
- More difficult error handling

#### Prompt Strategies

##### Template-Based Approach
```python
SYSTEM_PROMPTS = {
    'problem_solving': """
    You are a STEM tutor. Analyze the provided problem and:
    1. Identify the type of problem
    2. Break down the solution into clear steps
    3. Show all calculations
    4. Explain key concepts used
    
    Format your response in JSON:
    {
        "problem_type": str,
        "steps": [
            {
                "explanation": str,
                "calculation": str,
                "concepts": [str]
            }
        ]
    }
    """,
    'definition': """
    You are helping complete definitions in student notes.
    Given a partial definition, provide:
    1. The complete definition
    2. Key terms
    3. Related concepts
    
    Format as JSON:
    {
        "completion": str,
        "key_terms": [str],
        "related": [str]
    }
    """
}
```

##### Context-Aware Approach
```python
class ContextAwarePrompting:
    async def generate_prompt(self, content: str, task_type: str, context: Dict):
        """Generate prompt based on user's context and history."""
        base_prompt = SYSTEM_PROMPTS[task_type]
        
        # Add subject context
        if context.get('subject'):
            base_prompt += f"\nSubject area: {context['subject']}"
            
        # Add difficulty level
        if context.get('level'):
            base_prompt += f"\nTarget level: {context['level']}"
            
        # Add relevant previous problems
        if context.get('history'):
            base_prompt += "\nRelated previous work:"
            for item in context['history'][-3:]:
                base_prompt += f"\n- {item}"
                
        return base_prompt
```

#### Response Parsing Strategies

##### Structured JSON Response
```python
class JSONResponseParser:
    def parse_solution(self, response: str) -> Dict:
        """Parse structured JSON response."""
        try:
            data = json.loads(response)
            return SolutionSchema.validate(data)
        except json.JSONDecodeError:
            return self._fallback_parser(response)
```

##### Markdown Response
```python
class MarkdownResponseParser:
    def parse_solution(self, response: str) -> Dict:
        """Parse markdown-formatted response."""
        sections = response.split('##')
        return {
            'overview': sections[0].strip(),
            'steps': self._parse_steps(sections[1:]),
            'conclusion': sections[-1].strip()
        }
```

#### Caching Strategies

##### Simple Cache
```python
class SimpleCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        
    async def get_cached_response(self, content: str, task_type: str) -> Optional[str]:
        """Get cached response if available."""
        cache_key = f"{task_type}:{hashlib.md5(content.encode()).hexdigest()}"
        return await self.redis.get(cache_key)
```

##### Smart Cache
```python
class SmartCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        
    async def get_similar_response(self, content: str, task_type: str) -> Optional[str]:
        """Find similar cached problems/definitions."""
        similar_keys = await self._find_similar_keys(content)
        if similar_keys:
            return await self._merge_similar_responses(similar_keys)
```

#### Error Handling

```python
class RobustClaudeAssistant:
    async def safe_query(self, content: str, task_type: str) -> Result:
        try:
            return await self._process_with_retry(content, task_type)
        except APIError as e:
            return self._handle_api_error(e)
        except ParseError as e:
            return self._handle_parse_error(e)
        except Exception as e:
            return self._handle_unexpected_error(e)
            
    async def _process_with_retry(self, content: str, task_type: str) -> Result:
        """Implement exponential backoff retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                return await self._process_request(content, task_type)
            except RetryableError as e:
                await self._wait_before_retry(attempt)
```

## Feature Implementation Details

### Problem Solving Flow
1. User writes a problem on the canvas
2. System either:
   - Automatically detects when problem is complete, or
   - User clicks "Solve" button next to detected problem
3. Right sidebar opens with step-by-step solution
4. Each step includes:
   - Explanation in plain language
   - Mathematical calculations
   - Key concepts used
   - (Future) Visual aids/diagrams

### Definition Autocomplete
1. System monitors for definition indicators:
   - Phrases like "is defined as", "refers to"
   - Term followed by dash or colon
   - Bullet points under concept headings
2. Shows subtle completion suggestion inline
3. User can:
   - Accept with tab/enter
   - Continue writing to ignore
   - (Future) Choose from multiple suggestions

### Note Reorganization
1. User clicks "Improve Notes" button
2. System:
   - Analyzes document structure
   - Identifies key concepts
   - Reorganizes for logical flow
   - Adds missing context
   - Enhances formatting
3. Shows preview with accept/reject option

## API Design

### REST Endpoints

```
POST /api/v1/notes
  - Create new note
  
PUT /api/v1/notes/{id}
  - Update existing note
  
POST /api/v1/recognition
  - Process handwriting
  
POST /api/v1/assist
  - Get AI suggestions
```

### WebSocket Events

```
stroke:update
  - Real-time stroke data
  
recognition:result
  - OCR results
  
assist:suggestion
  - AI assistant updates
```

## Data Models

```typescript
interface Note {
  id: string;
  content: StrokeData[];
  recognizedText: string;
  suggestions: Suggestion[];
  metadata: {
    created: Date;
    updated: Date;
    version: number;
  }
}

interface StrokeData {
  points: Point[];
  pressure: number;
  timestamp: number;
}
```

## Development Timeline

### Week 1-2: Foundation
- Setup project structure
- Implement basic canvas system
- Create API endpoints

### Week 3-4: Core Features
- Integrate handwriting recognition
- Implement basic AI suggestions
- Build real-time sync system

### Week 5-6: MVP Polish
- Performance optimization
- Error handling
- Basic offline support

## Technical Dependencies

### External APIs
- MyScript API (handwriting recognition)
- Anthropic Claude API (AI assistance)
- S3 (file storage)

### Development Tools
- Docker for containerization
- GitHub Actions for CI/CD
- ESLint + Prettier for code quality

## Monitoring & Debugging

### Logging
```python
logger = logging.getLogger(__name__)

async def process_recognition(stroke_data):
    logger.info(f"Processing stroke: {stroke_data.id}")
    try:
        result = await recognition_pipeline.process(stroke_data)
        logger.debug(f"Recognition result: {result}")
        return result
    except RecognitionError as e:
        logger.error(f"Recognition failed: {e}")
        raise
```

### Error Handling
- Custom error types for different failure modes
- Graceful degradation for API failures
- Offline fallback mechanisms

## Performance Considerations

### Optimization Strategies
1. Stroke data compression
2. Incremental recognition updates
3. Efficient canvas rendering
4. Background processing for AI suggestions

### Caching Strategy
```python
@cache.memoize(timeout=3600)
async def get_suggestion(content: str) -> Suggestion:
    return await ai_service.generate_suggestion(content)
```

## Future Technical Considerations

### Scaling
- Horizontal scaling via k8s
- Database sharding strategy
- CDN integration for static assets

### Enhanced Features
- Collaborative editing support
- Real-time multiplayer capabilities
- Advanced offline support

## Development Environment

### Local Setup
```bash
# Development environment setup
docker-compose up -d
npm install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Testing Strategy
- Jest for frontend unit tests
- Pytest for backend testing
- Cypress for E2E testing
