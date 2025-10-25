# System Architecture

## Overview

The Assistive Communication Device implements a real-time visual lip movement recognition system designed to help people with speech impairments communicate more effectively.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OpenCV Video Display + Keyboard Controls             │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────────┐
│                Processing Pipeline                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Video Capture (Camera Module)                     │  │
│  │     - Webcam input                                    │  │
│  │     - Frame buffering                                 │  │
│  │     - Hardware acceleration (AMD Ryzen AI)            │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  2. Lip Detection (Computer Vision)                   │  │
│  │     - MediaPipe Face Mesh                             │  │
│  │     - Facial landmark detection                       │  │
│  │     - Lip movement tracking                           │  │
│  │     - Movement pattern analysis                       │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  3. Text Processing (Llama 2)                         │  │
│  │     - Movement pattern classification                 │  │
│  │     - Phoneme mapping                                 │  │
│  │     - Text generation                                 │  │
│  │     - Context-aware completion                        │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  4. Speech Synthesis (TTS)                            │  │
│  │     - Text-to-Speech conversion                       │  │
│  │     - Audio output                                    │  │
│  │     - Real-time feedback                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Camera Capture Module (`src/utils/camera.py`)

**Purpose**: Captures video feed from webcam with optimized performance

**Key Features**:
- Multi-threaded frame capture for better FPS
- Hardware acceleration support (AMD Ryzen AI)
- Configurable resolution and frame rate
- Frame buffering to prevent dropped frames

**Technologies**:
- OpenCV for video capture
- Threading for non-blocking operation
- AMD Ryzen AI hardware acceleration

### 2. Lip Detection Module (`src/lip_detection/`)

**Purpose**: Detects and tracks lip movements in real-time

**Key Features**:
- Facial landmark detection using MediaPipe
- 21-point lip contour tracking
- Movement magnitude calculation
- Pattern history tracking

**Technologies**:
- MediaPipe Face Mesh (468 facial landmarks)
- OpenCV for image processing
- NumPy for numerical computations

**Algorithm**:
1. Detect face in frame using MediaPipe
2. Extract lip landmark coordinates (upper and lower lips)
3. Calculate vertical distance between lips
4. Track movement magnitude over time
5. Detect significant movements

### 3. Text Processing Module (`src/text_processing/`)

**Purpose**: Converts lip movements to text using Llama 2

**Key Features**:
- Movement pattern analysis
- Phoneme mapping
- Text generation with Llama 2
- Context-aware predictions
- Sentence completion

**Technologies**:
- Transformers library (HuggingFace)
- Llama 2 language model
- PyTorch for inference
- Hardware acceleration (GPU/AMD Ryzen AI)

**Processing Pipeline**:
1. Analyze movement pattern (small, medium, large, rapid)
2. Map pattern to phoneme
3. Buffer phonemes
4. Generate coherent text using Llama 2
5. Provide word predictions

### 4. Speech Synthesis Module (`src/speech_synthesis/`)

**Purpose**: Converts recognized text to speech output

**Key Features**:
- Multiple TTS engine support
- Asynchronous speech output
- Adjustable rate and volume
- Natural-sounding voices

**Technologies**:
- pyttsx3 (offline, cross-platform)
- gTTS (online, Google TTS)
- pygame for audio playback

### 5. Utility Modules (`src/utils/`)

**Configuration Loader** (`config_loader.py`):
- JSON-based configuration
- Runtime parameter management
- Default settings with overrides

**Camera Utilities** (`camera.py`):
- Video capture abstraction
- Performance monitoring
- Resource management

## Data Flow

1. **Video Capture**: Camera captures frame → Frame queue
2. **Face Detection**: Frame → MediaPipe → Facial landmarks
3. **Lip Tracking**: Landmarks → Lip coordinates → Movement magnitude
4. **Pattern Analysis**: Movement history → Pattern classification
5. **Text Generation**: Pattern → Phoneme → Text buffer → Llama 2 → Completed text
6. **Speech Output**: Text → TTS engine → Audio output
7. **Visual Feedback**: All data → OpenCV display → User

## AMD Ryzen AI Integration

### Hardware Acceleration Features

1. **Video Processing**:
   - Hardware-accelerated video decoding
   - GPU-accelerated frame processing
   - Optimized memory transfers

2. **AI Inference**:
   - ROCm support for PyTorch
   - GPU acceleration for Llama 2
   - Optimized neural network execution

3. **Performance Optimization**:
   - Multi-threading for parallel processing
   - Efficient memory management
   - Reduced latency through hardware acceleration

### Configuration

Enable AMD Ryzen AI features in `config/default_config.json`:

```json
"amd_ryzen_ai": {
  "enable_hardware_acceleration": true,
  "use_gpu": true,
  "optimize_for_ryzen": true
}
```

## Performance Considerations

### Real-time Requirements

- **Target FPS**: 30 fps for smooth operation
- **Latency**: < 100ms for responsive feedback
- **Memory**: 2-4 GB for basic operation, 16+ GB for Llama 2

### Optimization Strategies

1. **Frame Processing**: Multi-threaded capture to separate I/O from processing
2. **Model Inference**: GPU acceleration for Llama 2
3. **Memory Management**: Frame buffering with size limits
4. **Async Operations**: Non-blocking speech synthesis

## Extensibility

### Adding New Features

1. **Custom Movement Patterns**: Extend `TextProcessor.movement_patterns`
2. **Alternative Models**: Replace Llama 2 with other language models
3. **Additional TTS Engines**: Implement new synthesizer backends
4. **Enhanced Detection**: Add emotion detection, head pose estimation

### Integration Points

- **Model Interface**: Easy to swap Llama 2 for other LLMs
- **TTS Interface**: Pluggable text-to-speech engines
- **Detection Interface**: Alternative lip reading algorithms

## Security & Privacy

- **Local Processing**: All video processing happens locally
- **No Cloud Dependency**: Core functionality works offline (except gTTS)
- **No Data Collection**: No user data is stored or transmitted
- **Model Privacy**: Llama 2 runs locally when downloaded

## Future Enhancements

1. **Improved Lip Reading**: Deep learning-based lip reading models
2. **Word Recognition**: Direct word-level recognition from lip movements
3. **Multi-language Support**: Recognition and synthesis in multiple languages
4. **Mobile Deployment**: Port to mobile devices with neural engines
5. **Cloud Option**: Optional cloud-based processing for resource-constrained devices
