"""
Simple test for music generation service.
Usage: python backend/tests/test_music_generation.py
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.music_generation import generate_music

# Test song data (using the format from your teammate's example)
TEST_SONG = {
    "song_title": "Hire Me! (Test Song)",
    "genre": "Modern Pop, Radio-Friendly, Catchy",
    "bpm": 115,
    "mood": "Upbeat, confident, optimistic",
    "vocal_style": "Male pop vocals, clear, melodic, contemporary",
    "instrumentation": "Pop production with synths, electronic drums, bass, bright synth pads",
    "scenes": [
        {
            "scene_num": 1,
            "time_range": "0-5s",
            "description": "Intro/Hook",
            "lyrics": "I'm the one you're looking for",
            "musical_mood": "Bright synth intro, upbeat drums kick in, catchy pop melody"
        },
        {
            "scene_num": 2,
            "time_range": "5-10s",
            "description": "Skills Showcase",
            "lyrics": "Full-stack ready, skills on point",
            "musical_mood": "Building energy, pop beat intensifies, confident vocal delivery"
        },
        {
            "scene_num": 3,
            "time_range": "10-15s",
            "description": "Experience Highlight",
            "lyrics": "Five years strong, shipped to scale",
            "musical_mood": "Full pop production, maximum energy, infectious melody"
        },
        {
            "scene_num": 4,
            "time_range": "15-20s",
            "description": "Company Connection",
            "lyrics": "Your mission, my passion now",
            "musical_mood": "Chorus hook, memorable melody, radio-ready sound"
        },
        {
            "scene_num": 5,
            "time_range": "20-25s",
            "description": "Value Proposition",
            "lyrics": "Watch me make your vision real",
            "musical_mood": "Bridge section, slightly stripped back, building anticipation"
        },
        {
            "scene_num": 6,
            "time_range": "25-30s",
            "description": "Call to Action",
            "lyrics": "Just say yes, hire me!",
            "musical_mood": "Big pop finale, all elements together, strong memorable ending"
        }
    ]
}

# Test
print("Testing music generation...")
print(f"Song: {TEST_SONG['song_title']}")
print(f"Genre: {TEST_SONG['genre']} | BPM: {TEST_SONG['bpm']}")
print("\nGenerating 30-second track... (takes ~30-60 seconds)\n")

result = generate_music(TEST_SONG)

if result['status'] == 'success':
    print("\n✅ Done!")
    print(f"Duration: {result['duration_seconds']} seconds")
    print(f"Audio size: {len(result['audio_data']) / 1024:.2f} KB")
    
    # Save the audio file
    output_path = os.path.join(BACKEND_DIR, "tests", "test_files", "generated_music.mp3")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        f.write(result['audio_data'])
    
    print(f"\n💾 Audio saved to: {output_path}")
    print("\nYou can now play the generated music file!")
else:
    print("\n❌ Failed!")
    print(f"Error: {result.get('error', 'Unknown error')}")

