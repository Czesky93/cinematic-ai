#!/usr/bin/env python3
"""Demo test for CinematicAI video generation"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from cinematic_ai.core.video_generator import CinematicAI


def run_demo():
    """Run demo video generation"""
    print("=" * 60)
    print("Cinematic AI - Demo Test")
    print("=" * 60)
    
    # Setup paths
    base_dir = Path(__file__).parent
    script_path = base_dir / "scripts" / "sample_script.txt"
    characters_dir = base_dir / "characters"
    locations_dir = base_dir / "locations"
    output_path = base_dir / "output" / "demo_video.mp4"
    
    # Verify demo files exist
    if not script_path.exists():
        print(f"Error: Script not found at {script_path}")
        return 1
    
    if not characters_dir.exists():
        print(f"Error: Characters directory not found at {characters_dir}")
        return 1
    
    if not locations_dir.exists():
        print(f"Error: Locations directory not found at {locations_dir}")
        return 1
    
    print(f"\nDemo Configuration:")
    print(f"  Script: {script_path}")
    print(f"  Characters: {characters_dir}")
    print(f"  Locations: {locations_dir}")
    print(f"  Output: {output_path}")
    print()
    
    try:
        # Initialize and run
        generator = CinematicAI()
        output_video = generator.generate_video(
            script_path=str(script_path),
            characters_dir=str(characters_dir),
            locations_dir=str(locations_dir),
            output_path=str(output_path)
        )
        
        print("\n" + "=" * 60)
        print("✓ Demo completed successfully!")
        print(f"✓ Video created at: {output_video}")
        
        # Check file size
        if os.path.exists(output_video):
            size_mb = os.path.getsize(output_video) / (1024 * 1024)
            print(f"✓ File size: {size_mb:.2f} MB")
        
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n✗ Demo failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_demo())
