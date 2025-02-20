# ScriptO iOS Frontend Documentation

## ⚠️ License Notice

```
Copyright (c) 2025 Michael Gorman
All rights reserved.

This documentation is made public for viewing and educational purposes only.
No permission is granted for any use, modification, or distribution
without explicit written permission from the copyright holder.
```

## Overview
ScriptO iOS is a note-taking application that combines traditional handwriting capabilities with AI-powered STEM problem-solving and term definitions.

## Core Features

### Note Management
- Digital notepad with drawing capabilities
- Multiple paper styles (lined, grid, blank)
- File organization system
- Tags and subjects for easy categorization
- Real-time saving
- Export/share functionality

### Drawing Tools
- Pen tool with customizable stroke width and color
- Highlighter tool for text selection
- Eraser tool
- Selection tool for moving/resizing content
- Shape tools (circles, squares, lines)
- Text insertion tool

### AI Integration
- Text selection via highlight tool
- Two-action context menu:
  1. "Solve Problem" - Sends highlighted text to STEM solver
  2. "Define Term" - Requests definition for highlighted text
- AI response display in side panel or overlay
- Response history tracking

## Technical Architecture

### State Management
```swift
class NoteState {
    var currentNote: Note
    var drawingMode: DrawingMode
    var selectedTool: Tool
    var aiContext: AIContext
    var userPreferences: UserPreferences
}

enum DrawingMode {
    case draw
    case highlight
    case erase
    case select
}
```

### Data Models
```swift
struct Note {
    let id: UUID
    var title: String
    var content: [DrawingElement]
    var tags: [String]
    var subject: String
    var created: Date
    var modified: Date
}

struct DrawingElement {
    let id: UUID
    var type: ElementType
    var points: [CGPoint]
    var strokeProperties: StrokeProperties
    var bounds: CGRect
}

struct AIInteraction {
    let id: UUID
    var type: AIInteractionType
    var status: Status
    var request: String
    var response: String?
    var error: String?
}
```

### Network Layer
```swift
protocol APIClient {
    func authenticate(username: String, password: String) -> AnyPublisher<AuthResponse, Error>
    func createNote(note: Note) -> AnyPublisher<NoteResponse, Error>
    func updateNote(id: UUID, note: Note) -> AnyPublisher<NoteResponse, Error>
    func solveProblem(text: String) -> AnyPublisher<AIResponse, Error>
    func defineTerm(text: String) -> AnyPublisher<AIResponse, Error>
}
```

## API Integration

### Authentication
```swift
class AuthManager {
    func login(username: String, password: String) async throws -> Token
    func refreshToken() async throws -> Token
    func logout() async
}
```

### Note Operations
```swift
class NoteManager {
    func createNote(title: String, subject: String) async throws -> Note
    func saveNote(note: Note) async throws
    func deleteNote(id: UUID) async throws
    func getNotes(skip: Int, limit: Int) async throws -> [Note]
    func searchNotes(query: String) async throws -> [Note]
}
```

### AI Operations
```swift
class AIManager {
    func solveProblem(text: String) async throws -> AIResponse
    func defineTerm(text: String) async throws -> AIResponse
    func getInteractionStatus(id: UUID) async throws -> AIStatus
}
```

## User Interface Components

### Main Views
1. NotesListView
   - Grid/list of note thumbnails
   - Search bar
   - Sorting options
   - New note button

2. NoteEditorView
   - Drawing canvas
   - Tool palette
   - Color picker
   - Paper style selector
   - AI response panel

3. AIResponseView
   - Problem/term display
   - Solution/definition display
   - Loading states
   - Error handling

### Navigation
```swift
enum AppScreen {
    case notesList
    case noteEditor(UUID?)
    case settings
    case aiHistory
}
```

## Data Persistence

### Local Storage
- Notes cached using Core Data
- User preferences in UserDefaults
- Offline drawing support
- Background sync when online

### Sync Strategy
1. Real-time drawing stroke sync
2. Periodic full note sync
3. Conflict resolution with server version
4. Background upload for AI interactions

## Error Handling
```swift
enum AppError {
    case network(Error)
    case authentication(Error)
    case drawing(Error)
    case aiProcessing(Error)
    case storage(Error)
}
```

## Performance Considerations
1. Drawing optimization
   - Stroke smoothing
   - Path simplification
   - Layer compositing

2. Memory management
   - Page splitting for large notes
   - Image compression
   - Resource cleanup

3. Network efficiency
   - Request batching
   - Response caching
   - Incremental loading

## Security
1. Secure storage of auth tokens
2. Biometric authentication option
3. Data encryption at rest
4. Secure network communication

## Testing Strategy
1. Unit tests for managers
2. UI tests for drawing
3. Integration tests for API
4. Performance tests for drawing
5. Offline functionality tests

## Future Improvements
1. Apple Pencil pressure sensitivity
2. Multi-window support on iPad
3. Handwriting recognition
4. Real-time collaboration
5. Document scanning
6. Voice notes
7. Custom paper templates
8. Advanced shape recognition
