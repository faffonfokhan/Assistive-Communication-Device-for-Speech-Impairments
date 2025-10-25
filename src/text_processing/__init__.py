"""
Text Processing Module
Handles text generation and processing using Llama 2
"""

try:
    from .processor import TextProcessor
    __all__ = ['TextProcessor']
except ImportError:
    __all__ = []
