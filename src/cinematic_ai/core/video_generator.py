"""Main video generator orchestrating all components"""
import os
from pathlib import Path
from typing import Optional, List
from .config import Config
from .script_parser import ScriptParser
from .character_manager import CharacterManager
from .frame_generator import FrameGenerator
from .audio_generator import AudioGenerator
from .video_assembler import VideoAssembler
from ..utils.logger import setup_logging, get_logger


class CinematicAI:
    """Main class for generating cinematic videos from scripts"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize CinematicAI
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = Config(config_path)
        
        # Setup logging
        self.logger = setup_logging(self.config)
        self.logger.info("Initializing CinematicAI...")
        
        # Initialize components
        self.script_parser = ScriptParser(self.config)
        self.audio_generator = AudioGenerator(self.config)
        self.video_assembler = VideoAssembler(self.config)
        
        # These will be initialized when processing
        self.character_manager = None
        self.frame_generator = None
    
    def generate_video(self, script_path: str, characters_dir: str, 
                      locations_dir: str, output_path: str,
                      background_music: Optional[str] = None) -> str:
        """
        Generate video from script and assets
        
        Args:
            script_path: Path to script file
            characters_dir: Directory with character images
            locations_dir: Directory with location images
            output_path: Path for output video
            background_music: Optional background music file
            
        Returns:
            Path to generated video
        """
        self.logger.info("=" * 60)
        self.logger.info("Starting video generation process")
        self.logger.info("=" * 60)
        
        # Initialize managers
        self.character_manager = CharacterManager(characters_dir)
        self.frame_generator = FrameGenerator(self.config, locations_dir)
        
        # Step 1: Parse script
        self.logger.info("Step 1: Parsing script...")
        with open(script_path, 'r') as f:
            script_text = f.read()
        scenes = self.script_parser.parse_script(script_text)
        
        if not scenes:
            raise ValueError("No scenes found in script")
        
        # Step 2: Process each scene
        self.logger.info(f"Step 2: Processing {len(scenes)} scenes...")
        scenes_data = []
        
        temp_dir = Path(self.config.get('output.temp_directory', 'demo/output/temp'))
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        for scene in scenes:
            self.logger.info(f"\nProcessing Scene {scene.number}: {scene.location}")
            
            # Get character images for this scene
            character_images = []
            for char_name in scene.characters:
                char_img = self.character_manager.get_character_image(char_name)
                if char_img:
                    character_images.append(char_img)
                    self.logger.info(f"  - Using character: {char_name}")
            
            # Generate frames
            self.logger.info(f"  - Generating frames...")
            frames = self.frame_generator.generate_scene_frames(
                scene, character_images, str(temp_dir)
            )
            
            # Generate voiceover
            self.logger.info(f"  - Generating voiceover...")
            audio_path = temp_dir / f"scene_{scene.number}_audio.mp3"
            self.audio_generator.generate_voiceover(scene.dialogue, str(audio_path))
            
            scenes_data.append({
                'scene': scene,
                'frames': frames,
                'audio': str(audio_path)
            })
        
        # Step 3: Assemble video
        self.logger.info("\nStep 3: Assembling final video...")
        output_video = self.video_assembler.create_video(
            scenes_data, output_path, background_music
        )
        
        self.logger.info("=" * 60)
        self.logger.info(f"Video generation complete!")
        self.logger.info(f"Output: {output_video}")
        self.logger.info("=" * 60)
        
        return output_video
