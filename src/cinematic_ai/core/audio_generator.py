"""Audio generator for TTS and audio mixing"""
import os
from pathlib import Path
from typing import Optional
from gtts import gTTS
from ..utils.logger import get_logger

logger = get_logger('audio_generator')


class AudioGenerator:
    """Generates TTS voiceovers and handles audio mixing"""
    
    def __init__(self, config):
        """
        Initialize audio generator
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.tts_lang = config.get('audio.tts_language', 'en')
        self.tts_slow = config.get('audio.tts_slow', False)
    
    def generate_voiceover(self, text: str, output_path: str) -> str:
        """
        Generate TTS voiceover from text
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file
        """
        try:
            logger.info(f"Generating TTS voiceover: {len(text)} characters")
            
            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Generate TTS
            tts = gTTS(text=text, lang=self.tts_lang, slow=self.tts_slow)
            tts.save(output_path)
            
            logger.info(f"Voiceover saved to: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating TTS: {e}")
            # Create silent audio as fallback
            return self._create_silent_audio(output_path)
    
    def _create_silent_audio(self, output_path: str, duration: float = 1.0) -> str:
        """Create a silent audio file as fallback"""
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # Create very quiet tone
            silent = Sine(20).to_audio_segment(duration=int(duration * 1000), volume=-50)
            silent.export(output_path, format="mp3")
            logger.info(f"Created fallback silent audio: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error creating silent audio: {e}")
            return output_path
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert ms to seconds
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 5.0  # Default fallback
