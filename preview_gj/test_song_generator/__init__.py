"""
Test Song Generator - ElevenLabs Music API testing module.
Generates 30-second structured songs with 6 scenes.
"""

from .elevenlabs_music_api import ElevenLabsMusicClient, create_elevenlabs_client
from .example_lyrics import ALL_EXAMPLES, EXAMPLE_SONG_1, EXAMPLE_SONG_2, EXAMPLE_SONG_3

__all__ = [
    "ElevenLabsMusicClient",
    "create_elevenlabs_client",
    "ALL_EXAMPLES",
    "EXAMPLE_SONG_1",
    "EXAMPLE_SONG_2",
    "EXAMPLE_SONG_3",
]
