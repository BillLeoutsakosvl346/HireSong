"""
Music generation service using ElevenLabs Music API.
Generates 30-second songs from structured prompts.
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any
from elevenlabs import ElevenLabs


def _ensure_elevenlabs_key():
    """Load .env and ensure ELEVENLABS_API_KEY is available."""
    here = os.path.dirname(__file__)
    dotenv_path = os.path.abspath(os.path.join(here, '..', '..', '.env'))
    load_dotenv(dotenv_path)
    
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY not found. Please set it in backend/.env")
    return key


def _build_music_prompt(song_data: Dict) -> str:
    """
    Build a comprehensive, structured prompt from song data.
    
    Args:
        song_data: Dictionary with genre, bpm, mood, scenes, etc.
    
    Returns:
        Comprehensive prompt string for ElevenLabs Music API
    """
    prompt_parts = []
    
    # Header with overall musical specifications
    prompt_parts.append(f"Genre: {song_data['genre']}")
    prompt_parts.append(f"Tempo: {song_data['bpm']} BPM")
    prompt_parts.append(f"Mood: {song_data['mood']}")
    prompt_parts.append(f"Vocal Style: {song_data['vocal_style']}")
    prompt_parts.append(f"Instrumentation: {song_data['instrumentation']}")
    prompt_parts.append(f"Total Duration: 30 seconds (6 scenes × ~5 seconds each)\n")
    
    # Scene-by-scene breakdown with timing markers
    for scene in song_data['scenes']:
        prompt_parts.append(f"[Scene {scene['scene_num']}: {scene['time_range']} - {scene['description']}]")
        prompt_parts.append(f"Lyrics: {scene['lyrics']}")
        prompt_parts.append(f"Music: {scene['musical_mood']}\n")
    
    # Instructions for consistency
    prompt_parts.append(
        "IMPORTANT: Maintain consistent tempo and genre throughout all 6 scenes. "
        "Each scene should be approximately 5 seconds. Ensure smooth transitions between scenes. "
        "The music should flow seamlessly as one complete 30-second track."
    )
    
    return "\n".join(prompt_parts)


def generate_music(song_data: Dict) -> Dict[str, Any]:
    """
    Generate a complete 30-second song from structured song data.
    
    Args:
        song_data: Dictionary containing:
            - song_title: Title of the song
            - genre: Musical genre
            - bpm: Beats per minute
            - mood: Overall mood
            - vocal_style: Vocal description
            - instrumentation: Instrumentation description
            - scenes: List of 6 scene dictionaries with timing, lyrics, and mood
    
    Returns:
        Dictionary with:
            - status: "success" or "failed"
            - audio_data: Raw audio bytes (MP3)
            - duration_seconds: Duration of the track
            - metadata: Song metadata
    """
    _ensure_elevenlabs_key()
    
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
    # Build the comprehensive prompt
    full_prompt = _build_music_prompt(song_data)
    
    print(f"\n🎵 Generating music: {song_data['song_title']}")
    print(f"   Genre: {song_data['genre']}")
    print(f"   BPM: {song_data['bpm']} | Mood: {song_data['mood']}")
    print(f"   This may take 30-60 seconds...\n")
    
    try:
        # Generate music using ElevenLabs SDK
        # music_length_ms = 30000 for 30 seconds
        audio_generator = client.music.compose(
            prompt=full_prompt,
            music_length_ms=30000
        )
        
        # Collect all audio chunks into bytes
        audio_data = b''
        for chunk in audio_generator:
            audio_data += chunk
        
        print(f"✅ Music generation complete!")
        print(f"   Audio size: {len(audio_data) / 1024:.2f} KB")
        
        return {
            "status": "success",
            "song_title": song_data['song_title'],
            "genre": song_data['genre'],
            "bpm": song_data['bpm'],
            "duration_seconds": 30,
            "audio_data": audio_data,
            "metadata": {
                "mood": song_data['mood'],
                "vocal_style": song_data['vocal_style'],
                "instrumentation": song_data['instrumentation'],
                "num_scenes": len(song_data['scenes'])
            }
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Music generation failed: {error_msg}")
        
        return {
            "status": "failed",
            "error": error_msg
        }

