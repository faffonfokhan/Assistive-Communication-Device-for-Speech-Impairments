# Usage Guide

## Basic Usage

### Starting the Application

```bash
python main.py
```

This will start the application with default settings:
- Camera ID: 0 (default webcam)
- Configuration: config/default_config.json
- Without Llama 2 model (basic mode)

### Command Line Options

```bash
python main.py --help
```

Available options:
- `--config PATH`: Specify custom configuration file
- `--camera ID`: Select camera device (default: 0)

### Examples

Use a different camera:
```bash
python main.py --camera 1
```

Use custom configuration:
```bash
python main.py --config my_config.json
```

## Interactive Controls

While the application is running:

- **`q`**: Quit the application
- **`s`**: Speak the currently recognized text
- **`r`**: Reset/clear the text buffer

## Features

### 1. Lip Movement Detection

The system uses computer vision to detect and track lip movements in real-time:
- Green dots show detected lip landmarks
- Yellow line shows lip contour
- Movement magnitude is displayed on screen

### 2. Text Processing

Recognized lip movements are converted to text:
- Simple phoneme mapping in basic mode
- Advanced text generation with Llama 2 model
- Context-aware predictions

### 3. Speech Synthesis

Generated text is converted to speech:
- Automatic periodic speech output
- Manual trigger with 's' key
- Adjustable speech rate and volume

### 4. AMD Ryzen AI Optimization

Hardware acceleration features:
- GPU-accelerated inference
- Optimized video processing
- Enhanced performance on Ryzen AI PCs

## Configuration

### Configuration File

Edit `config/default_config.json` to customize:

```json
{
  "camera": {
    "device_id": 0,
    "width": 640,
    "height": 480,
    "fps": 30
  },
  "lip_detection": {
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
    "movement_threshold": 2.0
  },
  "text_processing": {
    "model_name": "meta-llama/Llama-2-7b-chat-hf",
    "use_local": false
  },
  "speech_synthesis": {
    "engine": "pyttsx3",
    "rate": 150,
    "volume": 1.0
  }
}
```

### Camera Settings

- **device_id**: Camera device ID (0 for default webcam)
- **width/height**: Resolution (640x480 recommended)
- **fps**: Frame rate (30 fps recommended)

### Lip Detection Settings

- **min_detection_confidence**: Face detection threshold (0.0-1.0)
- **min_tracking_confidence**: Face tracking threshold (0.0-1.0)
- **movement_threshold**: Minimum movement to detect (pixels)

### Text Processing Settings

- **model_name**: HuggingFace model identifier for Llama 2
- **use_local**: Use local model path instead of downloading
- **context_window**: Number of recent phonemes to keep

### Speech Synthesis Settings

- **engine**: TTS engine ('pyttsx3' or 'gtts')
- **rate**: Speech rate in words per minute
- **volume**: Volume level (0.0-1.0)

## Using Llama 2

To enable advanced text generation with Llama 2:

1. Ensure you have HuggingFace authentication set up
2. When starting the application, answer 'y' to load the model
3. Wait for model loading (may take several minutes)
4. The system will use Llama 2 for text completion and prediction

Note: Llama 2 requires significant computational resources:
- 16GB+ RAM recommended
- GPU recommended for real-time performance
- First run will download the model (~13GB for 7B variant)

## Performance Tips

### For Best Performance

1. Use AMD Ryzen AI PC with hardware acceleration enabled
2. Ensure good lighting for face detection
3. Position camera at eye level
4. Minimize background movement
5. Use GPU acceleration for Llama 2 inference

### Troubleshooting Performance Issues

- Lower camera resolution in config
- Reduce FPS if processing is slow
- Skip Llama 2 loading for faster startup
- Close other resource-intensive applications

## Advanced Usage

### Custom Model Integration

To use a different Llama 2 variant:

1. Update `model_name` in config
2. Ensure model is compatible with transformers
3. Check model requirements (RAM, GPU)

Example models:
- `meta-llama/Llama-2-7b-chat-hf` (default)
- `meta-llama/Llama-2-13b-chat-hf` (better quality, more resources)

### Speech Engine Selection

#### pyttsx3 (Default)
- Offline, no internet required
- Fast and responsive
- Platform-dependent voices

#### gTTS
- Online, requires internet
- Natural-sounding voices
- Slight delay for audio generation

Change in config:
```json
"speech_synthesis": {
  "engine": "gtts"
}
```

## Accessibility Features

- Large, clear on-screen text display
- Visual feedback for lip detection
- Adjustable speech rate
- Keyboard shortcuts for easy control
- Real-time performance monitoring

## Support

For issues, questions, or contributions, please visit:
https://github.com/faffonfokhan/Assistive-Communication-Device-for-Speech-Impairments
