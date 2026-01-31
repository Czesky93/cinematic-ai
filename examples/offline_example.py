"""
Example demonstrating offline mode and fallback behavior
"""
import sys
from pathlib import Path

# Add src to path for running as script
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from cinematic_ai.core.video_generator import CinematicAI


def main():
    """
    This example demonstrates the offline fallback capability.
    
    When internet is unavailable:
    - TTS will fail gracefully and use silent audio fallback
    - All other operations work offline (frame generation, video assembly)
    - The video will still be created successfully
    """
    
    print("=" * 70)
    print("Cinematic AI - Offline Mode Example")
    print("=" * 70)
    print()
    print("This example shows how Cinematic AI works in offline mode:")
    print("- Frame generation: Works offline (uses local images)")
    print("- TTS voiceover: Attempts online, falls back to silent audio")
    print("- Video assembly: Works offline (uses local FFmpeg)")
    print()
    
    # Setup paths
    base_dir = Path(__file__).parent.parent
    script_path = base_dir / "demo" / "scripts" / "sample_script.txt"
    characters_dir = base_dir / "demo" / "characters"
    locations_dir = base_dir / "demo" / "locations"
    output_path = base_dir / "demo" / "output" / "offline_example.mp4"
    
    try:
        # Initialize and run
        generator = CinematicAI()
        
        print("Starting video generation...")
        print(f"  Script: {script_path.name}")
        print(f"  Output: {output_path}")
        print()
        
        output_video = generator.generate_video(
            script_path=str(script_path),
            characters_dir=str(characters_dir),
            locations_dir=str(locations_dir),
            output_path=str(output_path)
        )
        
        print()
        print("=" * 70)
        print("✓ Success!")
        print(f"✓ Video created: {output_video}")
        print()
        print("Note: If you see 'Error generating TTS' above, that's expected")
        print("      when offline. The video was still created successfully")
        print("      using silent audio as a fallback.")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
