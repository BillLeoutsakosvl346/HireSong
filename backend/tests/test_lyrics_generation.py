"""
Simple test for lyrics generation service.
Usage: python backend/tests/test_lyrics_generation.py
"""

import sys
import os
import json

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.lyrics_generation import generate_song_lyrics

# Test prompts
TEST_CV_SUMMARY = """
Name: Alex Chen
Contact: alex.chen@email.com

EDUCATION
- B.S. Computer Science, Stanford University (2018-2022)
- GPA: 3.8/4.0

WORK EXPERIENCE
• Software Engineer at Google (2022-2024)
  - Built recommendation system that improved CTR by 15%
  - Led team of 3 engineers on Cloud Storage optimization
  - Reduced API latency by 40% through caching improvements

• ML Intern at OpenAI (Summer 2021)
  - Worked on GPT-3 fine-tuning pipeline
  - Implemented data preprocessing tools in Python

SKILLS
- Languages: Python, JavaScript, Go, SQL
- Technologies: React, Node.js, TensorFlow, Docker, Kubernetes
- Cloud: AWS, GCP
"""

TEST_COMPANY_SUMMARY = """
Anthropic is an AI safety company building reliable, interpretable, and steerable AI systems.

Products:
- Claude: Advanced AI assistant focused on safety and helpfulness
- API for developers to integrate Claude into their applications

Mission & Values:
- AI Safety is the core focus
- Building beneficial AI that is helpful, harmless, and honest
- Research-driven approach to AI development
- Strong emphasis on constitutional AI and alignment

Culture:
- Collaborative research environment
- Focus on solving hard technical problems
- Commitment to responsible AI development

Technologies:
- Large language models
- Reinforcement learning from human feedback (RLHF)
- Constitutional AI techniques
- Scalable oversight methods

Looking for:
- Strong engineering and research skills
- Passion for AI safety and alignment
- Experience with ML systems and infrastructure
"""


# Test 1: No genre specified (AI chooses)
print("=" * 80)
print("TEST 1: AI-selected genre (Surprise Me)")
print("=" * 80)
print(f"\nCV Summary Preview: {TEST_CV_SUMMARY[:150]}...")
print(f"\nCompany Summary Preview: {TEST_COMPANY_SUMMARY[:150]}...")
print("\nGenerating song lyrics... (takes ~10-15 seconds)\n")

song = generate_song_lyrics(TEST_CV_SUMMARY, TEST_COMPANY_SUMMARY)

print("\n✅ Success!")
print("\n" + "=" * 80)
print("GENERATED SONG STRUCTURE")
print("=" * 80)

print(f"\n🎵 Title: {song.song_title}")
print(f"🎸 Genre: {song.genre}")
print(f"🥁 BPM: {song.bpm}")
print(f"😊 Mood: {song.mood}")
print(f"🎤 Vocal Style: {song.vocal_style}")
print(f"🎹 Instrumentation: {song.instrumentation}")

print("\n" + "-" * 80)
print("SCENES (6 × 5 seconds each)")
print("-" * 80)

for scene in song.scenes:
    print(f"\n[Scene {scene.scene_num}: {scene.time_range}] - {scene.description}")
    print(f"  Lyrics: \"{scene.lyrics}\"")
    word_count = len(scene.lyrics.split())
    print(f"  Word count: {word_count} {'✅' if word_count <= 12 else '⚠️ (too long!)'}")
    print(f"  Musical mood: {scene.musical_mood}")

print("\n" + "=" * 80)

# Save to file for reference
output_file = os.path.join(BACKEND_DIR, "tests", "test_files", "generated_lyrics.json")
with open(output_file, 'w') as f:
    json.dump(song.model_dump(), f, indent=2)
print(f"\n💾 Saved to: {output_file}")

# Test 2: With specific genre
print("\n\n" + "=" * 80)
print("TEST 2: User-selected genre (Rap)")
print("=" * 80)
print("\nGenerating Rap song lyrics... (takes ~10-15 seconds)\n")

rap_song = generate_song_lyrics(TEST_CV_SUMMARY, TEST_COMPANY_SUMMARY, preferred_genre="Rap")

print("\n✅ Success!")
print("\n" + "=" * 80)
print("GENERATED RAP SONG STRUCTURE")
print("=" * 80)

print(f"\n🎵 Title: {rap_song.song_title}")
print(f"🎸 Genre: {rap_song.genre} {'✅' if 'rap' in rap_song.genre.lower() or 'hip' in rap_song.genre.lower() else '⚠️ (should be Rap!)'}")
print(f"🥁 BPM: {rap_song.bpm}")
print(f"😊 Mood: {rap_song.mood}")
print(f"🎤 Vocal Style: {rap_song.vocal_style}")
print(f"🎹 Instrumentation: {rap_song.instrumentation}")

print("\n" + "-" * 80)
print("SCENES (6 × 5 seconds each)")
print("-" * 80)

for scene in rap_song.scenes:
    print(f"\n[Scene {scene.scene_num}: {scene.time_range}] - {scene.description}")
    print(f"  Lyrics: \"{scene.lyrics}\"")
    word_count = len(scene.lyrics.split())
    print(f"  Word count: {word_count} {'✅' if 15 <= word_count <= 20 else '⚠️ (expected 15-20 for Rap!)'}")
    print(f"  Musical mood: {scene.musical_mood}")

print("\n" + "=" * 80)

# Save rap version
rap_output_file = os.path.join(BACKEND_DIR, "tests", "test_files", "generated_lyrics_rap.json")
with open(rap_output_file, 'w') as f:
    json.dump(rap_song.model_dump(), f, indent=2)
print(f"\n💾 Saved rap version to: {rap_output_file}")

