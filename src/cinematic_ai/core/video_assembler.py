"""Video assembler using FFmpeg and MoviePy"""
import os
from pathlib import Path
from typing import List, Optional
try:
    # Try MoviePy 2.x imports
    from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
except ImportError:
    # Fallback to MoviePy 1.x imports
    from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

from ..utils.logger import get_logger

logger = get_logger('video_assembler')


class VideoAssembler:
    """Assembles final video from frames and audio"""
    
    def __init__(self, config):
        """
        Initialize video assembler
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.fps = config.get('video.fps', 24)
        self.width = config.get('video.resolution.width', 1920)
        self.height = config.get('video.resolution.height', 1080)
        self.max_duration = config.get('video.max_duration', 300)
        self.codec = config.get('video.codec', 'libx264')
    
    def create_video(self, scenes_data: List[dict], output_path: str,
                     background_music: Optional[str] = None) -> str:
        """
        Create final video from scene data
        
        Args:
            scenes_data: List of dicts with 'frames' and 'audio' paths
            output_path: Path to save output video
            background_music: Optional path to background music
            
        Returns:
            Path to created video
        """
        logger.info(f"Assembling video with {len(scenes_data)} scenes")
        
        # Create output directory
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        video_clips = []
        total_duration = 0
        
        for i, scene_data in enumerate(scenes_data):
            logger.info(f"Processing scene {i+1}/{len(scenes_data)}")
            
            # Get scene duration from audio
            audio_path = scene_data.get('audio')
            frames = scene_data.get('frames', [])
            
            if not frames:
                logger.warning(f"No frames for scene {i+1}, skipping")
                continue
            
            # Calculate scene duration
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                scene_duration = audio_clip.duration
                audio_clip.close()
            else:
                # Default duration per frame
                scene_duration = len(frames) * self.config.get('frame_generation.slideshow.image_duration', 5)
            
            # Check if we exceed max duration
            if total_duration + scene_duration > self.max_duration:
                logger.warning(f"Reached max duration limit, stopping at scene {i+1}")
                break
            
            # Create clip from frames
            scene_clip = self._create_scene_clip(frames, scene_duration, audio_path)
            
            if scene_clip:
                video_clips.append(scene_clip)
                total_duration += scene_duration
        
        if not video_clips:
            logger.error("No video clips created")
            raise ValueError("No valid scenes to create video")
        
        # Concatenate all scenes
        logger.info("Concatenating video clips...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Add background music if provided
        if background_music and os.path.exists(background_music):
            logger.info("Adding background music...")
            final_video = self._add_background_music(final_video, background_music)
        
        # Write final video
        logger.info(f"Writing final video to {output_path}")
        final_video.write_videofile(
            output_path,
            fps=self.fps,
            codec=self.codec,
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None  # Suppress moviepy's verbose output
        )
        
        # Clean up
        final_video.close()
        for clip in video_clips:
            clip.close()
        
        logger.info(f"Video created successfully: {output_path}")
        return output_path
    
    def _create_scene_clip(self, frames: List[str], duration: float, 
                          audio_path: Optional[str] = None):
        """Create a video clip from frames with audio"""
        try:
            if len(frames) == 1:
                # Single frame - create static clip
                clip = ImageClip(frames[0], duration=duration)
            else:
                # Multiple frames - create slideshow
                frame_duration = duration / len(frames)
                frame_clips = [
                    ImageClip(frame, duration=frame_duration) 
                    for frame in frames
                ]
                clip = concatenate_videoclips(frame_clips, method="compose")
            
            # Set resolution - MoviePy 2.x uses resized(), 1.x uses resize()
            try:
                clip = clip.resized((self.width, self.height))
            except AttributeError:
                clip = clip.resize((self.width, self.height))
            
            # Add audio if available
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                # MoviePy 2.x uses with_audio(), 1.x uses set_audio()
                try:
                    clip = clip.with_audio(audio)
                except AttributeError:
                    clip = clip.set_audio(audio)
            
            return clip
        
        except Exception as e:
            logger.error(f"Error creating scene clip: {e}")
            return None
    
    def _add_background_music(self, video_clip, music_path: str):
        """Add background music to video clip"""
        try:
            bg_music = AudioFileClip(music_path)
            
            # Loop background music if video is longer
            if bg_music.duration < video_clip.duration:
                n_loops = int(video_clip.duration / bg_music.duration) + 1
                bg_music_clips = [bg_music] * n_loops
                # MoviePy 2.x and 1.x audio concatenation
                try:
                    from moviepy import concatenate_audioclips
                    bg_music = concatenate_audioclips(bg_music_clips)
                except ImportError:
                    # Fallback for MoviePy 1.x
                    from moviepy.editor import concatenate_audioclips
                    bg_music = concatenate_audioclips(bg_music_clips)
                
                # Trim to match video duration
                try:
                    bg_music = bg_music.with_subclip(0, video_clip.duration)
                except AttributeError:
                    bg_music = bg_music.subclip(0, video_clip.duration)
            else:
                try:
                    bg_music = bg_music.with_subclip(0, video_clip.duration)
                except AttributeError:
                    bg_music = bg_music.subclip(0, video_clip.duration)
            
            # Adjust volume - MoviePy 2.x uses with_effects
            bg_volume = self.config.get('audio.background_music_volume', 0.3)
            try:
                bg_music = bg_music.with_volume_scaled(bg_volume)
            except AttributeError:
                bg_music = bg_music.volumex(bg_volume)
            
            # Mix with existing audio
            if video_clip.audio:
                final_audio = CompositeAudioClip([video_clip.audio, bg_music])
            else:
                final_audio = bg_music
            
            # Set audio on clip
            try:
                return video_clip.with_audio(final_audio)
            except AttributeError:
                return video_clip.set_audio(final_audio)
        
        except Exception as e:
            logger.error(f"Error adding background music: {e}")
            return video_clip
