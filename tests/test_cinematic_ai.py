"""Unit tests for CinematicAI components"""
import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from cinematic_ai.core.config import Config
from cinematic_ai.core.script_parser import ScriptParser, Scene


class TestConfig(unittest.TestCase):
    """Test configuration loading"""
    
    def test_config_loads(self):
        """Test that default config loads"""
        config = Config()
        self.assertIsNotNone(config.config)
        self.assertEqual(config.get('video.fps'), 24)
    
    def test_config_get(self):
        """Test config get with dot notation"""
        config = Config()
        fps = config.get('video.fps')
        self.assertEqual(fps, 24)
        
        # Test default value
        missing = config.get('nonexistent.key', 'default')
        self.assertEqual(missing, 'default')


class TestScriptParser(unittest.TestCase):
    """Test script parsing"""
    
    def test_parse_formal_script(self):
        """Test parsing formal screenplay format"""
        script = """
INT. COFFEE SHOP - DAY

SARAH sits at a table.

JOHN enters.

EXT. PARK - NIGHT

They walk together.
"""
        parser = ScriptParser()
        scenes = parser.parse_script(script)
        
        self.assertEqual(len(scenes), 2)
        self.assertEqual(scenes[0].location, "COFFEE SHOP")
        self.assertEqual(scenes[0].time, "DAY")
        self.assertEqual(scenes[1].location, "PARK")
        self.assertEqual(scenes[1].time, "NIGHT")
    
    def test_parse_simple_script(self):
        """Test parsing simple script format"""
        script = """
This is the first scene with some dialogue.

This is the second scene with more content.

And here is the third scene.
"""
        parser = ScriptParser()
        scenes = parser.parse_script(script)
        
        self.assertEqual(len(scenes), 3)
        self.assertEqual(scenes[0].number, 1)
        self.assertEqual(scenes[1].number, 2)
        self.assertEqual(scenes[2].number, 3)
    
    def test_scene_creation(self):
        """Test Scene object creation"""
        scene = Scene(
            number=1,
            location="COFFEE SHOP",
            time="DAY",
            dialogue="SARAH sits at a table.",
            characters=["SARAH"]
        )
        
        self.assertEqual(scene.number, 1)
        self.assertEqual(scene.location, "COFFEE SHOP")
        self.assertEqual(scene.time, "DAY")
        self.assertIn("SARAH", scene.characters)


class TestCharacterManager(unittest.TestCase):
    """Test character management"""
    
    def test_character_manager_initialization(self):
        """Test that character manager initializes"""
        from cinematic_ai.core.character_manager import CharacterManager
        
        # Should not crash with non-existent directory
        manager = CharacterManager("nonexistent_dir")
        self.assertEqual(len(manager.characters), 0)


if __name__ == '__main__':
    unittest.main()
