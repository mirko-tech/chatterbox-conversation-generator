"""
Dialogue Generator Module

Handles parsing and structuring dialogue data from text files.
This module is responsible only for text-based dialogue structure,
not for audio generation.
"""

import re
from typing import List, Dict, Optional
from pathlib import Path


class DialogueParser:
    """
    Parses dialogue files and creates structured dialogue data.

    File format expected:
        voice1_wav="path/to/voice1.wav"
        voice2_wav="path/to/voice2.wav"

        voice1="Hello, how are you?"
        voice2="I'm fine, thanks. And you?"
        voice1="Very well!"
    """

    def __init__(self, voices_dir: str = "voices"):
        """
        Initialize the dialogue parser.

        Args:
            voices_dir: Directory containing voice template files
        """
        self.voices_dir = Path(voices_dir)

    def parse_dialogue_file(self, filepath: str) -> List[Dict]:
        """
        Read and parse a dialogue file.

        Args:
            filepath: Path to the dialogue file

        Returns:
            List of dialogue turns, each containing:
            - voice: voice identifier (e.g., "voice1")
            - voice_path: path to the voice template WAV file
            - text: text to be spoken

        Raises:
            FileNotFoundError: If the dialogue file doesn't exist
            ValueError: If no dialogue lines are found in the file
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Dialogue file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract voice template paths
        voice_paths = self._extract_voice_paths(content)

        # Extract dialogue lines
        dialogue_lines = self._extract_dialogue_lines(content, voice_paths)

        if len(dialogue_lines) == 0:
            raise ValueError(
                "No dialogue lines found in file. "
                "Ensure the file contains:\n"
                "1. Voice definitions: voice1_wav=\"path/to/voice.wav\"\n"
                "2. Dialogue lines: voice1=\"Text to speak\""
            )

        # Validate and warn about short text
        for i, line in enumerate(dialogue_lines, 1):
            if len(line['text'].strip()) < 3:
                print(f"WARNING: Line {i} has very short text ('{line['text']}') "
                      f"and may cause TTS errors. Consider using longer phrases.")

        return dialogue_lines

    def _extract_voice_paths(self, content: str) -> Dict[str, str]:
        """
        Extract voice template paths from dialogue content.

        Args:
            content: Raw dialogue file content

        Returns:
            Dictionary mapping voice names to their template paths
        """
        voice_paths = {}
        voice_pattern = r'(voice\d+)_wav\s*=\s*["\']([^"\']+)["\']'

        for match in re.finditer(voice_pattern, content):
            voice_name = match.group(1)
            voice_path = match.group(2)
            voice_paths[voice_name] = voice_path

        return voice_paths

    def _extract_dialogue_lines(self, content: str,
                                voice_paths: Dict[str, str]) -> List[Dict]:
        """
        Extract dialogue lines from content.

        Args:
            content: Raw dialogue file content
            voice_paths: Dictionary of voice name to path mappings

        Returns:
            List of dialogue turn dictionaries
        """
        dialogue_lines = []

        # Updated pattern to handle quotes properly
        # Matches: voice1="text" or voice1='text'
        # Handles apostrophes inside the text by matching the opening quote type
        dialogue_pattern = r'(voice\d+)\s*=\s*"([^"]+)"|' + r"(voice\d+)\s*=\s*'([^']+)'"

        for match in re.finditer(dialogue_pattern, content):
            # Check which group matched (double quotes or single quotes)
            if match.group(1):  # Double quotes
                voice_name = match.group(1)
                text = match.group(2)
            else:  # Single quotes
                voice_name = match.group(3)
                text = match.group(4)

            # Only add lines that have an associated voice path
            if voice_name in voice_paths:
                dialogue_lines.append({
                    'voice': voice_name,
                    'voice_path': voice_paths[voice_name],
                    'text': text
                })

        return dialogue_lines


def load_dialogue(dialogue_file: str, voices_dir: str = "voices") -> List[Dict]:
    """
    Convenience function to load and parse a dialogue file.

    Args:
        dialogue_file: Path to the dialogue file
        voices_dir: Directory containing voice templates

    Returns:
        List of dialogue turns with voice and text information

    Example:
        >>> dialogue = load_dialogue("examples/conversation.txt")
        >>> for turn in dialogue:
        ...     print(f"{turn['voice']}: {turn['text']}")
    """
    parser = DialogueParser(voices_dir=voices_dir)
    return parser.parse_dialogue_file(dialogue_file)
