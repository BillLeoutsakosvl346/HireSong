import asyncio
from typing import Dict, Optional
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY


class ElevenLabsMusicClient:
    """
    Client for interacting with ElevenLabs Music API using the official SDK.
    Generates a complete 30-second song in a single API call with scene-based structure.
    """
    
    def __init__(self, api_key: str):
        self.client = ElevenLabs(api_key=api_key)
    
    def _build_comprehensive_prompt(
        self,
        song_data: Dict
    ) -> str:
        """
        Build a comprehensive, structured prompt from the song data.
        The prompt includes scene markers for timing (0-5s, 5-10s, etc.)
        and detailed musical instructions for consistency.
        
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
    
    async def generate_song(
        self,
        song_data: Dict
    ) -> Dict:
        """
        Generate a complete 30-second song from structured song data.
        Uses a single API call with comprehensive scene-based prompt.
        
        Args:
            song_data: Dictionary containing:
                - theme: Song theme/identifier
                - song_title: Title of the song
                - genre: Musical genre
                - bpm: Beats per minute
                - mood: Overall mood
                - vocal_style: Vocal description
                - instrumentation: Instrumentation description
                - scenes: List of 6 scene dictionaries with timing, lyrics, and mood
        
        Returns:
            Dictionary with generated song metadata and audio data
        """
        # Build the comprehensive prompt
        full_prompt = self._build_comprehensive_prompt(song_data)
        
        print(f"\n🎵 Starting song generation: {song_data['song_title']}")
        print(f"📝 Genre: {song_data['genre']}")
        print(f"🎼 BPM: {song_data['bpm']} | Mood: {song_data['mood']}\n")
        print("📋 Prompt Preview:")
        print("-" * 80)
        print(full_prompt[:500] + "..." if len(full_prompt) > 500 else full_prompt)
        print("-" * 80 + "\n")
        
        try:
            print("🔄 Calling ElevenLabs Music API using client.music.compose()...")
            
            # Use the official SDK method to generate music
            # music_length_ms = 30000 for 30 seconds
            # This returns a generator of audio chunks
            audio_generator = await asyncio.to_thread(
                self.client.music.compose,
                prompt=full_prompt,
                music_length_ms=30000  # 30 seconds in milliseconds
            )
            
            # Read all chunks from the generator into bytes
            audio_data = b''
            for chunk in audio_generator:
                audio_data += chunk
            
            print(f"✅ Song generated successfully!")
            
            result = {
                "status": "success",
                "song_title": song_data['song_title'],
                "theme": song_data['theme'],
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
            
            print(f"\n📊 Generation Result:")
            print(f"   Song Title: {result.get('song_title', 'N/A')}")
            print(f"   Duration: 30 seconds")
            print(f"   Audio Data Size: {len(audio_data) / 1024:.2f} KB")
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Generation failed: {error_msg}")
            
            return {
                "status": "failed",
                "error": error_msg
            }


async def create_elevenlabs_client() -> ElevenLabsMusicClient:
    """Factory function to create an ElevenLabs Music API client."""
    return ElevenLabsMusicClient(ELEVENLABS_API_KEY)
