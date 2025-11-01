"""
Simple test for scene planning service.
Usage: python backend/tests/test_scene_planning.py
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

from api.services.scene_planning import generate_scene_plan

# Test prompts (same as lyrics generation test)
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

# Load the generated lyrics
print("Testing scene planning...")
print("\nLoading generated lyrics from previous test...\n")

lyrics_file = os.path.join(BACKEND_DIR, "tests", "test_files", "generated_lyrics.json")

if not os.path.exists(lyrics_file):
    print(f"❌ Lyrics file not found: {lyrics_file}")
    print("\nPlease run test_lyrics_generation.py first to generate lyrics!")
    exit(1)

with open(lyrics_file, 'r') as f:
    lyrics_data = json.load(f)

print(f"✅ Loaded lyrics: '{lyrics_data['song_title']}'")
print(f"   Genre: {lyrics_data['genre']} | BPM: {lyrics_data['bpm']}")
print("\nGenerating visual scene plans... (takes ~15-20 seconds)\n")

# Generate scene plan
scene_plan = generate_scene_plan(TEST_CV_SUMMARY, TEST_COMPANY_SUMMARY, lyrics_data)

print("\n✅ Success!")
print("\n" + "=" * 80)
print("GENERATED SCENE PLAN")
print("=" * 80)

for scene in scene_plan.scenes:
    print(f"\n{'='*80}")
    print(f"SCENE {scene.scene_num}: {scene.time_range}")
    print(f"{'='*80}")
    
    print(f"\n📝 Scene Description:")
    print(f"   {scene.scene_description}")
    
    print(f"\n🖼️  Image Prompt (for Nano Banana):")
    print(f"   {scene.image_prompt}")
    
    print(f"\n🎬 Video Prompt (for Kling):")
    print(f"   {scene.video_prompt}")

print("\n" + "=" * 80)

# Save to file
output_file = os.path.join(BACKEND_DIR, "tests", "test_files", "generated_scenes.json")
with open(output_file, 'w') as f:
    json.dump(scene_plan.model_dump(), f, indent=2)

print(f"\n💾 Saved to: {output_file}")
print("\n✨ Scene planning complete! Ready for image and video generation.")

