"""
Configuration Loader
Loads and manages application configuration
"""

import json
import os


class ConfigLoader:
    """
    Configuration loader and manager
    """
    
    def __init__(self, config_path=None):
        """
        Initialize config loader
        
        Args:
            config_path: Path to configuration file
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'default_config.json')
        
        self.config_path = config_path
        self.config = self._load_default_config()
        
        if os.path.exists(config_path):
            self.load_config(config_path)
    
    def _load_default_config(self):
        """Load default configuration"""
        return {
            'camera': {
                'device_id': 0,
                'width': 640,
                'height': 480,
                'fps': 30
            },
            'lip_detection': {
                'min_detection_confidence': 0.5,
                'min_tracking_confidence': 0.5,
                'movement_threshold': 2.0
            },
            'text_processing': {
                'model_name': 'meta-llama/Llama-2-7b-chat-hf',
                'use_local': False,
                'context_window': 10
            },
            'speech_synthesis': {
                'engine': 'pyttsx3',
                'rate': 150,
                'volume': 1.0
            },
            'amd_ryzen_ai': {
                'enable_hardware_acceleration': True,
                'use_gpu': True,
                'optimize_for_ryzen': True
            },
            'ui': {
                'window_width': 800,
                'window_height': 600,
                'show_landmarks': True,
                'show_movement_info': True
            }
        }
    
    def load_config(self, config_path):
        """
        Load configuration from file
        
        Args:
            config_path: Path to JSON config file
        """
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                # Merge with default config
                self._merge_config(self.config, loaded_config)
            print(f"Configuration loaded from {config_path}")
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Using default configuration")
    
    def _merge_config(self, base, update):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def save_config(self, config_path=None):
        """
        Save current configuration to file
        
        Args:
            config_path: Path to save config (uses default if None)
        """
        if config_path is None:
            config_path = self.config_path
        
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration saved to {config_path}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key_path, default=None):
        """
        Get configuration value by path
        
        Args:
            key_path: Dot-separated path (e.g., 'camera.width')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """
        Set configuration value by path
        
        Args:
            key_path: Dot-separated path (e.g., 'camera.width')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_all(self):
        """Get entire configuration"""
        return self.config.copy()
