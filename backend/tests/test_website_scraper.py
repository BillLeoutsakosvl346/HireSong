"""
Simple test for website scraping and summarization.
Usage: python backend/tests/test_website_scraper.py [URL]

If no URL provided, uses a default test URL.
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.website_scraper import scrape_website
from api.services.summarization import summarize_company_website

# Get URL from command line or use default
if len(sys.argv) > 1:
    test_url = sys.argv[1]
else:
    # Default test URL
    test_url = "https://www.anthropic.com"

print("Testing website scraping and summarization...")
print(f"Target URL: {test_url}\n")

# Step 1: Scrape the website
print("=" * 60)
print("STEP 1: SCRAPING WEBSITE")
print("=" * 60)

try:
    scraped_text = scrape_website(test_url, max_chars=8000)
    
    print(f"\n📄 First 500 characters of scraped text:")
    print("-" * 60)
    print(scraped_text[:500] + "...")
    print("-" * 60)
    
except Exception as e:
    print(f"❌ Scraping failed: {e}")
    exit(1)

# Step 2: Summarize the website
print("\n" + "=" * 60)
print("STEP 2: SUMMARIZING WITH OPENAI")
print("=" * 60)
print()

try:
    summary = summarize_company_website(scraped_text)
    
    print("\n✅ Done!")
    print("\n" + "=" * 60)
    print("COMPANY SUMMARY")
    print("=" * 60)
    print(summary)
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"❌ Summarization failed: {e}")
    exit(1)

