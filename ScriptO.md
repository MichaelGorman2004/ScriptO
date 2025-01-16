# ScriptO Flutter Technical Design Document

## System Overview
ScriptO is a mobile-first note-taking application built with Flutter, combining handwriting recognition with real-time AI assistance for STEM subjects. While cross-platform capabilities are supported, the primary focus is on delivering an exceptional mobile experience, with tablet support being a key priority.

## Core Technical Requirements

### Frontend Architecture
- **Framework**: Flutter
  - *Rationale*: Cross-platform support, excellent performance, rich widget ecosystem
- **State Management**: Riverpod
  - *Rationale*: Better dependency injection, simpler than Provider, great for complex state
- **Local Storage**: Hive
  - *Rationale*: Fast NoSQL database, great for Flutter, supports complex objects

### Backend Architecture
- **Framework**: FastAPI (remains unchanged)
  - *Rationale*: High performance, async support, great for mobile APIs
- **Database**: PostgreSQL
- **Caching**: Redis

## Core Components

### 1. Note-Taking Interface

#### Canvas Implementation Options

##### Option 1: Flutter CustomPainter
```dart
class StrokesPainter extends CustomPainter {
  final List<Stroke> strokes;
  
  StrokesPainter(this.strokes);
  
  @override
  void paint(Canvas canvas, Size size) {
    for (final stroke in strokes) {
      final paint = Paint()
        ..color = stroke.color
        ..strokeWidth = stroke.width
        ..strokeCap = StrokeCap.round;
      
      canvas.drawPoints(
        PointMode.polygon,
        stroke.points,
        paint,
      );
    }
  }
  
  @override
  bool shouldRepaint(StrokesPainter oldDelegate) => 
    strokes != oldDelegate.strokes;
}
```
**Pros:**
- Native Flutter performance
- Full control over rendering
- Small package size

**Cons:**
- More complex to implement
- Need to handle all gestures manually

##### Option 2: flutter_drawing_board Package
```dart
class DrawingCanvas extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return DrawingBoard(
      controller: _controller,
      background: Container(color: Colors.white),
      strokeWidth: 2.0,
      onDrawStart: _handleDrawStart,
      onDrawEnd: _handleDrawEnd,
    );
  }
}
```
**Pros:**
- Many features built-in
- Easy to implement
- Good touch support

**Cons:**
- Less control over internals
- Dependent on package updates

#### Stroke Data Structure
```dart
@freezed
class Stroke with _$Stroke {
  const factory Stroke({
    required String id,
    required List<Offset> points,
    required Color color,
    required double width,
    required StrokeType type,
    required DateTime created,
  }) = _Stroke;
  
  factory Stroke.fromJson(Map<String, dynamic> json) => 
    _$StrokeFromJson(json);
}
```

### 2. Recognition Pipeline

#### Handwriting Recognition Integration
```dart
class RecognitionService {
  final MyScriptClient _client;
  
  Future<String> recognizeStrokes(List<Stroke> strokes) async {
    try {
      final response = await _client.recognize(
        strokes.map((s) => s.toMyScriptFormat()).toList(),
      );
      return response.text;
    } on MyScriptException catch (e) {
      // Fallback to local Tesseract
      return _recognizeLocally(strokes);
    }
  }
}
```

### 3. AI Assistant Integration

#### State Management with Riverpod
```dart
@riverpod
class AssistantState extends _$AssistantState {
  final _claudeService = ClaudeService();
  
  Stream<AssistantResponse> getSolution(String problem) async* {
    state = const AsyncValue.loading();
    
    try {
      await for (final chunk in _claudeService.streamSolution(problem)) {
        yield* Stream.value(AsyncValue.data(chunk));
      }
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}
```

#### UI Implementation
```dart
class AssistantPanel extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final solutionState = ref.watch(assistantStateProvider);
    
    return AnimatedSlide(
      offset: Offset(solutionState.isLoading ? 0 : 1, 0),
      child: Container(
        width: 300,
        child: solutionState.when(
          data: (solution) => SolutionView(solution),
          loading: () => LoadingIndicator(),
          error: (e, st) => ErrorView(e),
        ),
      ),
    );
  }
}
```

### 4. Offline Support

#### Local Storage with Hive
```dart
@HiveType(typeId: 0)
class Note extends HiveObject {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final List<Stroke> strokes;
  
  @HiveField(2)
  final String recognizedText;
  
  @HiveField(3)
  final DateTime lastModified;
}

class NoteRepository {
  final Box<Note> _box;
  
  Future<void> saveNote(Note note) async {
    await _box.put(note.id, note);
    // Queue for sync when online
    await _syncQueue.add(note.id);
  }
}
```

### 5. Sync System

#### Background Sync
```dart
class SyncService {
  final NoteRepository _repository;
  final ApiClient _api;
  
  Future<void> syncNotes() async {
    final queue = await _repository.getSyncQueue();
    
    for (final noteId in queue) {
      final note = await _repository.getNote(noteId);
      try {
        await _api.uploadNote(note);
        await _repository.markSynced(noteId);
      } catch (e) {
        // Handle error, retry later
      }
    }
  }
}
```

## Mobile-First Priorities

### Core Mobile Features
- Optimized for touch and stylus input
- Mobile-specific UI patterns (bottom sheets, FABs, etc.)
- Responsive to different screen sizes
- Battery and resource optimization
- Offline-first approach
- Haptic feedback for better drawing experience

### Tablet Optimization
- Split-view support
- Enhanced stylus features for tablets
- Optimized UI for larger screens
- Multi-window support (iPadOS/Android)

### iOS
- Apple Pencil support
- PencilKit integration (optional)
- iCloud backup integration

### Android
- S-Pen support for Samsung devices
- Stylus API integration
- Android backup service integration

## Performance Optimizations

### Drawing Optimization
```dart
class OptimizedStrokeManager {
  // Simplify points while drawing to reduce memory
  List<Offset> _optimizePoints(List<Offset> points) {
    return points.reducedByDistance(minDistance: 2.0);
  }
  
  // Batch render updates
  void addPoint(Offset point) {
    _points.add(point);
    if (_points.length > 10) {
      _optimizeAndUpdate();
    }
  }
}
```

### Memory Management
- Implement virtual scrolling for long notes
- Lazy load images and resources
- Cache commonly used UI elements

## Testing Strategy

### Unit Tests
```dart
void main() {
  group('Stroke Recognition Tests', () {
    test('should recognize basic shapes', () async {
      final service = RecognitionService();
      final strokes = createTestStrokes();
      
      final result = await service.recognizeStrokes(strokes);
      
      expect(result, contains('circle'));
    });
  });
}
```

### Widget Tests
```dart
void main() {
  testWidgets('Canvas should handle basic drawing', (tester) async {
    await tester.pumpWidget(DrawingCanvas());
    
    await tester.dragFrom(Offset(0, 0), Offset(100, 100));
    await tester.pumpAndSettle();
    
    expect(find.byType(CustomPaint), findsOneWidget);
  });
}
```

## Development Timeline

### Phase 1 (Weeks 1-2)
- Basic canvas implementation
- Stroke management
- Local storage setup

### Phase 2 (Weeks 3-4)
- Recognition integration
- AI assistant integration
- Basic UI/UX

### Phase 3 (Weeks 5-6)
- Offline support
- Sync system
- Performance optimization

## Future Considerations

### Mobile Enhancement Priorities
- Advanced mobile-specific features (widgets, quick actions)
- Deep integration with mobile OS features
- Mobile-optimized collaboration features
- Enhanced mobile performance optimizations

### Feature Extensions
- Real-time collaboration
- Cloud sync across devices
- Advanced stylus support
- AR integration for 3D diagrams

### Scaling Considerations
- Implement efficient data pagination
- Optimize asset loading
- Consider using compute isolates for heavy tasks
