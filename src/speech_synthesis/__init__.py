"""
Speech Synthesis Module
Handles text-to-speech conversion using OpenAI Whisper and related technologies
"""

try:
    from .synthesizer import SpeechSynthesizer
    __all__ = ['SpeechSynthesizer']
except ImportError:
    __all__ = []
