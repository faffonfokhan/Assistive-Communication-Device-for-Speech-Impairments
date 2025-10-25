"""
Lip Detection Module
Handles real-time lip movement detection and tracking
"""

try:
    from .detector import LipDetector
    __all__ = ['LipDetector']
except ImportError:
    __all__ = []
