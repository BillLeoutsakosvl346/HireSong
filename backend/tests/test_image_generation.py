"""
Simple test for image generation service.
Usage: python backend/tests/test_image_generation.py
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service (it needs FAL_KEY at import time)
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.image_generation import generate_image_from_prompt

# Quick test
print("Testing image generation...")

test_image = os.path.join(BACKEND_DIR, "tests", "test_images", "test_selfie.jpg")
prompt = "add sunglasses to the person"

print(f"Using image: {test_image}")
print(f"Prompt: '{prompt}'")
print("Generating... (takes ~10-20 seconds)\n")

result = generate_image_from_prompt(prompt, test_image)

print("✅ Done!")
print(f"Generated image: {result['images'][0]['url']}")
print(f"Description: {result.get('description', 'N/A')}")

