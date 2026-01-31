"""Command-line interface for CinematicAI"""
import click
import sys
from pathlib import Path
from .core.video_generator import CinematicAI


@click.command()
@click.option('--script', '-s', required=True, type=click.Path(exists=True),
              help='Path to script file')
@click.option('--characters', '-c', required=True, type=click.Path(exists=True),
              help='Directory containing character images')
@click.option('--locations', '-l', required=True, type=click.Path(exists=True),
              help='Directory containing location images')
@click.option('--output', '-o', required=True, type=click.Path(),
              help='Output video path (e.g., output.mp4)')
@click.option('--music', '-m', type=click.Path(exists=True),
              help='Background music file (optional)')
@click.option('--config', type=click.Path(exists=True),
              help='Custom configuration file (optional)')
def main(script, characters, locations, output, music, config):
    """
    Cinematic AI - Generate videos from scripts, character photos, and location photos.
    
    Example usage:
    
        cinematic-ai -s script.txt -c ./characters -l ./locations -o video.mp4
    
    Or with background music:
    
        cinematic-ai -s script.txt -c ./characters -l ./locations -o video.mp4 -m music.mp3
    """
    try:
        # Initialize generator
        generator = CinematicAI(config_path=config)
        
        # Generate video
        output_video = generator.generate_video(
            script_path=script,
            characters_dir=characters,
            locations_dir=locations,
            output_path=output,
            background_music=music
        )
        
        click.echo(f"\n✓ Success! Video created at: {output_video}")
        sys.exit(0)
        
    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
