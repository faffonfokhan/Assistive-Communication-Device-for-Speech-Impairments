"""
Speech Synthesis Module
Handles text-to-speech conversion using pyttsx3 and gTTS
"""

try:
    from .synthesizer import SpeechSynthesizer
    __all__ = ['SpeechSynthesizer']
except ImportError:
    __all__ = []
