"""
Simple test for CV extraction and summarization.
Usage: python backend/tests/test_cv_extraction.py

Requirements:
1. Put a test CV PDF in: backend/tests/test_files/test_cv.pdf
2. Set OPENAI_API_KEY in backend/.env
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.text_extraction import extract_text_from_pdf
from api.services.summarization import summarize_cv

# Test
print("Testing CV extraction and summarization...")

test_pdf = os.path.join(BACKEND_DIR, "tests", "test_files", "test_cv.pdf")

if not os.path.exists(test_pdf):
    print(f"❌ Test CV not found at: {test_pdf}")
    print("\nPlease add a test CV PDF:")
    print(f"   mkdir -p {os.path.dirname(test_pdf)}")
    print(f"   # Copy your test CV to {test_pdf}")
    exit(1)

print(f"Using CV: {test_pdf}\n")

# Step 1: Extract text
raw_text = extract_text_from_pdf(test_pdf)

# Step 2: Summarize with OpenAI
print()
summary = summarize_cv(raw_text)

print("\n✅ Done!")
print("\n" + "=" * 60)
print("CV SUMMARY")
print("=" * 60)
print(summary)

