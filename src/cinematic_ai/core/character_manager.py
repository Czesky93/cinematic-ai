"""Character consistency manager for tracking character appearances"""
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import os
from ..utils.logger import get_logger

logger = get_logger('character_manager')


class Character:
    """Represents a character with reference images"""
    
    def __init__(self, name: str, image_paths: List[str]):
        self.name = name
        self.image_paths = image_paths
        self.primary_image = image_paths[0] if image_paths else None
    
    def get_image(self, index: int = 0) -> Optional[str]:
        """Get character image by index"""
        if 0 <= index < len(self.image_paths):
            return self.image_paths[index]
        return self.primary_image


class CharacterManager:
    """Manages character reference images for consistency"""
    
    def __init__(self, characters_dir: str):
        """
        Initialize character manager
        
        Args:
            characters_dir: Directory containing character images
        """
        self.characters_dir = Path(characters_dir)
        self.characters: Dict[str, Character] = {}
        self._load_characters()
    
    def _load_characters(self):
        """Load character images from directory"""
        if not self.characters_dir.exists():
            logger.warning(f"Characters directory not found: {self.characters_dir}")
            return
        
        logger.info(f"Loading characters from {self.characters_dir}")
        
        # Group images by character name (folder or prefix)
        for item in self.characters_dir.iterdir():
            if item.is_dir():
                # Each subdirectory is a character
                character_name = item.name
                image_paths = [
                    str(img) for img in item.iterdir()
                    if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']
                ]
                if image_paths:
                    self.characters[character_name] = Character(character_name, image_paths)
                    logger.info(f"Loaded character '{character_name}' with {len(image_paths)} images")
            elif item.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                # Individual image - use filename as character name
                character_name = item.stem
                if character_name not in self.characters:
                    self.characters[character_name] = Character(character_name, [str(item)])
                    logger.info(f"Loaded character '{character_name}' from single image")
    
    def get_character(self, name: str) -> Optional[Character]:
        """Get character by name (case-insensitive)"""
        # Try exact match first
        if name in self.characters:
            return self.characters[name]
        
        # Try case-insensitive match
        for char_name, character in self.characters.items():
            if char_name.lower() == name.lower():
                return character
        
        return None
    
    def get_character_image(self, name: str, index: int = 0) -> Optional[str]:
        """Get character image path"""
        character = self.get_character(name)
        if character:
            return character.get_image(index)
        return None
    
    def list_characters(self) -> List[str]:
        """Get list of all character names"""
        return list(self.characters.keys())
