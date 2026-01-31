"""Configuration manager for Cinematic AI"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager that loads and provides access to config settings"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to custom config file, or None to use default
        """
        if config_path is None:
            # Use default config - look in multiple locations
            # First try from src/cinematic_ai/core
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "default_config.yaml"
            
            # If not found, try from working directory
            if not config_path.exists():
                config_path = Path("config/default_config.yaml")
            
            # If still not found, try relative to current file going up
            if not config_path.exists():
                base_dir = Path(__file__).parent.parent.parent.parent
                config_path = base_dir / "config" / "default_config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'video.fps')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access to config"""
        return self.get(key)
