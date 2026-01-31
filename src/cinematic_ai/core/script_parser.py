"""Script parser for splitting scripts into scenes"""
import re
from typing import List, Dict, Any
from ..utils.logger import get_logger

logger = get_logger('script_parser')


class Scene:
    """Represents a single scene in the script"""
    
    def __init__(self, number: int, location: str, time: str, 
                 dialogue: str, characters: List[str] = None):
        self.number = number
        self.location = location
        self.time = time
        self.dialogue = dialogue
        self.characters = characters or []
    
    def __repr__(self):
        return f"Scene {self.number}: {self.location} - {self.time}"


class ScriptParser:
    """Parser for movie scripts to extract scenes"""
    
    def __init__(self, config=None):
        self.config = config
        self.scenes = []
    
    def parse_script(self, script_text: str) -> List[Scene]:
        """
        Parse script text into scenes
        
        Args:
            script_text: Raw script text
            
        Returns:
            List of Scene objects
        """
        logger.info("Parsing script into scenes...")
        
        # Split by scene headers (INT./EXT. pattern)
        scene_pattern = r'((?:INT\.|EXT\.)[^\n]+)'
        parts = re.split(scene_pattern, script_text)
        
        scenes = []
        scene_num = 1
        
        # If no formal scene headers, split by paragraphs
        if len(parts) <= 1:
            scenes = self._parse_simple_script(script_text)
        else:
            # Process formal screenplay format
            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    header = parts[i].strip()
                    content = parts[i + 1].strip()
                    
                    # Extract location and time from header
                    location, time = self._parse_scene_header(header)
                    
                    # Extract characters and dialogue
                    characters = self._extract_characters(content)
                    
                    scene = Scene(
                        number=scene_num,
                        location=location,
                        time=time,
                        dialogue=content,
                        characters=characters
                    )
                    scenes.append(scene)
                    scene_num += 1
        
        logger.info(f"Parsed {len(scenes)} scenes from script")
        self.scenes = scenes
        return scenes
    
    def _parse_simple_script(self, script_text: str) -> List[Scene]:
        """Parse simple script format (paragraphs as scenes)"""
        paragraphs = [p.strip() for p in script_text.split('\n\n') if p.strip()]
        scenes = []
        
        for i, para in enumerate(paragraphs, 1):
            scene = Scene(
                number=i,
                location=f"Scene {i}",
                time="DAY",
                dialogue=para,
                characters=self._extract_characters(para)
            )
            scenes.append(scene)
        
        return scenes
    
    def _parse_scene_header(self, header: str) -> tuple:
        """Extract location and time from scene header"""
        # Example: "INT. COFFEE SHOP - DAY"
        parts = header.split('-')
        
        location = parts[0].strip()
        location = location.replace('INT.', '').replace('EXT.', '').strip()
        
        time = parts[1].strip() if len(parts) > 1 else "DAY"
        
        return location, time
    
    def _extract_characters(self, text: str) -> List[str]:
        """Extract character names from dialogue"""
        # Look for all-caps names (common in screenplays)
        characters = re.findall(r'\b([A-Z][A-Z\s]+)\b', text)
        # Filter out common non-character words
        stop_words = {'INT', 'EXT', 'DAY', 'NIGHT', 'FADE', 'CUT', 'TO'}
        characters = [c.strip() for c in characters if c.strip() not in stop_words]
        return list(set(characters))  # Remove duplicates
