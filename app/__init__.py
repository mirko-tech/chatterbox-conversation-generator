"""
Chatterbox Dialogue Generator

A Python package for generating synthetic dialogues and converting them
to audio using Chatterbox TTS voice cloning.

Main components:
- dialogue_generator: Parse and structure dialogue text files
- voice_pipeline: Generate audio using Chatterbox TTS
- main: CLI entry point
"""

__version__ = "1.0.0"

# Lazy imports to avoid requiring all dependencies upfront
__all__ = [
    "load_dialogue",
    "DialogueParser",
    "create_dialogue_audio",
    "VoicePipeline",
]


def __getattr__(name):
    """Lazy import to avoid loading heavy dependencies unless needed."""
    if name in ("load_dialogue", "DialogueParser"):
        from app.dialogue_generator import load_dialogue, DialogueParser
        globals()["load_dialogue"] = load_dialogue
        globals()["DialogueParser"] = DialogueParser
        return globals()[name]
    elif name in ("create_dialogue_audio", "VoicePipeline"):
        from app.voice_pipeline import create_dialogue_audio, VoicePipeline
        globals()["create_dialogue_audio"] = create_dialogue_audio
        globals()["VoicePipeline"] = VoicePipeline
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
