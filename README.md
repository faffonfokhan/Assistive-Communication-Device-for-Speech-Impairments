# Assistive Communication Device for Speech Impairments

Using visual-based lip movement recognition, Llama 2 for text processing, text-to-speech synthesis (pyttsx3, gTTS), and AMD Ryzen AI hardware acceleration, this project implements a real-time assistive communication device that monitors lip movements to enable faster communication for people with speech impairments.

## Features

- **Real-time Lip Movement Detection**: Computer vision-based lip reading using facial landmarks
- **Text Generation**: Llama 2 integration for intelligent text prediction and completion
- **Speech Synthesis**: Text-to-speech conversion using pyttsx3 and gTTS
- **Hardware Acceleration**: Optimized for AMD Ryzen AI PC for real-time performance
- **User-friendly Interface**: Simple interface for easy communication

## System Architecture

1. **Lip Movement Recognition Module**: Captures video feed and detects lip movements using facial landmark detection
2. **Text Processing Module**: Uses Llama 2 to interpret lip movements and generate coherent text
3. **Speech Output Module**: Converts recognized text to natural speech using TTS engines (pyttsx3, gTTS)
4. **AMD Ryzen AI Optimization**: Leverages hardware acceleration for real-time performance

## Requirements

- Python 3.8+
- AMD Ryzen AI PC (recommended for optimal performance)
- Webcam for video capture
- See `requirements.txt` for Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
.
├── src/
│   ├── lip_detection/      # Lip movement detection module
│   ├── text_processing/    # Llama 2 text processing
│   ├── speech_synthesis/   # Whisper speech output
│   └── utils/              # Utility functions
├── config/                 # Configuration files
├── models/                 # Model files (downloaded at runtime)
├── main.py                 # Main application entry point
└── requirements.txt        # Python dependencies
```

## License

MIT License
