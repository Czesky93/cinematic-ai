"""Frame generator for creating video frames"""
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from ..utils.logger import get_logger

logger = get_logger('frame_generator')


class FrameGenerator:
    """Generates frames for video scenes"""
    
    def __init__(self, config, locations_dir: str):
        """
        Initialize frame generator
        
        Args:
            config: Configuration object
            locations_dir: Directory containing location images
        """
        self.config = config
        self.locations_dir = Path(locations_dir)
        self.width = config.get('video.resolution.width', 1920)
        self.height = config.get('video.resolution.height', 1080)
        self.mode = config.get('frame_generation.mode', 'slideshow')
        
        # Load location images
        self.location_images = self._load_location_images()
    
    def _load_location_images(self) -> List[str]:
        """Load all location images from directory"""
        if not self.locations_dir.exists():
            logger.warning(f"Locations directory not found: {self.locations_dir}")
            return []
        
        images = []
        for item in self.locations_dir.iterdir():
            if item.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                images.append(str(item))
        
        logger.info(f"Loaded {len(images)} location images")
        return images
    
    def generate_scene_frames(self, scene, character_images: List[str] = None,
                            output_dir: str = None) -> List[str]:
        """
        Generate frames for a scene
        
        Args:
            scene: Scene object
            character_images: List of character image paths for this scene
            output_dir: Directory to save generated frames
            
        Returns:
            List of generated frame paths
        """
        if self.mode == 'slideshow':
            return self._generate_slideshow_frames(scene, character_images, output_dir)
        else:
            # AI mode - fallback to slideshow if AI unavailable
            logger.warning("AI frame generation not available, using slideshow mode")
            return self._generate_slideshow_frames(scene, character_images, output_dir)
    
    def _generate_slideshow_frames(self, scene, character_images: List[str] = None,
                                   output_dir: str = None) -> List[str]:
        """Generate frames using slideshow approach with images"""
        frames = []
        
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path("demo/output/temp")
            output_path.mkdir(parents=True, exist_ok=True)
        
        # Collect images for this scene
        images_to_use = []
        
        # Add character images
        if character_images:
            images_to_use.extend(character_images)
        
        # Add location image
        if self.location_images:
            # Try to match location name, otherwise use first location
            location_image = self._find_location_image(scene.location)
            if location_image:
                images_to_use.append(location_image)
        
        # If no images, create a text frame
        if not images_to_use:
            frame_path = output_path / f"scene_{scene.number}_frame_1.png"
            self._create_text_frame(scene, str(frame_path))
            frames.append(str(frame_path))
        else:
            # Create frames from images
            for i, img_path in enumerate(images_to_use):
                frame_path = output_path / f"scene_{scene.number}_frame_{i+1}.png"
                self._create_frame_from_image(img_path, str(frame_path))
                frames.append(str(frame_path))
        
        logger.info(f"Generated {len(frames)} frames for scene {scene.number}")
        return frames
    
    def _find_location_image(self, location: str) -> Optional[str]:
        """Find location image matching the scene location"""
        location_lower = location.lower()
        
        for img_path in self.location_images:
            img_name = Path(img_path).stem.lower()
            if location_lower in img_name or img_name in location_lower:
                return img_path
        
        # Return first location image as fallback
        return self.location_images[0] if self.location_images else None
    
    def _create_frame_from_image(self, image_path: str, output_path: str):
        """Create a frame from an image, resizing to target resolution"""
        try:
            img = Image.open(image_path)
            
            # Calculate aspect ratio preserving resize
            img_ratio = img.width / img.height
            target_ratio = self.width / self.height
            
            if img_ratio > target_ratio:
                # Image is wider, fit to height
                new_height = self.height
                new_width = int(self.height * img_ratio)
            else:
                # Image is taller, fit to width
                new_width = self.width
                new_height = int(self.width / img_ratio)
            
            # Resize and crop to center
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to target size
            left = (new_width - self.width) // 2
            top = (new_height - self.height) // 2
            img = img.crop((left, top, left + self.width, top + self.height))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(output_path)
            logger.debug(f"Created frame: {output_path}")
        except Exception as e:
            logger.error(f"Error creating frame from {image_path}: {e}")
            # Create fallback text frame
            self._create_text_frame(None, output_path, f"Image Error: {Path(image_path).name}")
    
    def _create_text_frame(self, scene, output_path: str, text: str = None):
        """Create a simple text frame"""
        img = Image.new('RGB', (self.width, self.height), color='black')
        draw = ImageDraw.Draw(img)
        
        if text is None and scene:
            text = f"Scene {scene.number}\n{scene.location}\n{scene.time}"
        elif text is None:
            text = "Cinematic AI"
        
        # Use default font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Draw text in center
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((self.width - text_width) // 2, (self.height - text_height) // 2)
        draw.text(position, text, fill='white', font=font)
        
        img.save(output_path)
        logger.debug(f"Created text frame: {output_path}")
