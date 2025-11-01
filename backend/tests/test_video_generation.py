"""
Simple test for video generation service.
Usage: python backend/tests/test_video_generation.py
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.video_generation import generate_video_from_image

# Test
print("Testing video generation from image...")

test_image = os.path.join(BACKEND_DIR, "tests", "test_images", "test_selfie.jpg")

if not os.path.exists(test_image):
    print(f"❌ Test image not found at: {test_image}")
    print("Please add test_selfie.jpg to backend/tests/test_images/")
    exit(1)

prompt = "make the person in the picture fall on his knees and beg"

print(f"Using image: {test_image}")
print(f"Prompt: '{prompt}'")
print("Generating 5-second video... (takes ~30-60 seconds)\n")

result = generate_video_from_image(
    prompt=prompt,
    image_path=test_image,
    duration="5",
    aspect_ratio="16:9"
)

print("\n✅ Done!")
print(f"Generated video: {result['video']['url']}")
print("\nDownload the video from the URL above to view it!")

