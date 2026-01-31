"""Logging configuration for Cinematic AI"""
import logging
import os
from pathlib import Path
from typing import Optional


def setup_logging(config=None, log_file: Optional[str] = None, level: str = "INFO"):
    """
    Setup logging for the application
    
    Args:
        config: Configuration object
        log_file: Path to log file
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    if config:
        log_file = config.get('logging.file', 'logs/cinematic_ai.log')
        level = config.get('logging.level', 'INFO')
        log_format = config.get('logging.format', 
                               '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file) if log_file else logging.NullHandler(),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('cinematic_ai')


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(f'cinematic_ai.{name}')
