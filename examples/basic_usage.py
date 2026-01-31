"""
Basic usage example for Cinematic AI
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from cinematic_ai.core.video_generator import CinematicAI


# Example 1: Basic video generation
def example_basic():
    """Most basic usage - just script and images"""
    generator = CinematicAI()
    
    generator.generate_video(
        script_path="demo/scripts/sample_script.txt",
        characters_dir="demo/characters",
        locations_dir="demo/locations",
        output_path="demo/output/basic_example.mp4"
    )
    print("✓ Basic video created!")


# Example 2: With custom configuration
def example_custom_config():
    """Using custom configuration file"""
    # First, you would create a custom config file
    # Then initialize with it:
    generator = CinematicAI(config_path="config/default_config.yaml")
    
    generator.generate_video(
        script_path="demo/scripts/sample_script.txt",
        characters_dir="demo/characters",
        locations_dir="demo/locations",
        output_path="demo/output/custom_config_example.mp4"
    )
    print("✓ Video with custom config created!")


# Example 3: With background music
def example_with_music():
    """Adding background music to the video"""
    generator = CinematicAI()
    
    generator.generate_video(
        script_path="demo/scripts/sample_script.txt",
        characters_dir="demo/characters",
        locations_dir="demo/locations",
        output_path="demo/output/with_music_example.mp4",
        background_music="path/to/music.mp3"  # Add your music file
    )
    print("✓ Video with background music created!")


if __name__ == '__main__':
    print("Cinematic AI - Usage Examples")
    print("=" * 50)
    
    # Run basic example
    print("\n1. Running basic example...")
    example_basic()
    
    # Uncomment to run other examples:
    # print("\n2. Running custom config example...")
    # example_custom_config()
    
    # print("\n3. Running background music example...")
    # example_with_music()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
