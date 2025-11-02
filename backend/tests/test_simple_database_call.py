"""
Simple test that mimics the orchestrator's database calls.
This is the minimal test to see if database integration works.
"""

import sys
import os
import asyncio

# Point sys.path at backend/
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

print("="*80)
print("SIMPLE DATABASE CALL TEST (mimics orchestrator)")
print("="*80)

# Import exactly like the orchestrator does
from api.services.database import (
    save_pipeline_start,
    update_pipeline_progress,
    save_pipeline_completion,
    save_pipeline_error
)

# Simulate what orchestrator does
async def test_pipeline():
    print("\n📊 Simulating orchestrator pipeline with database calls...\n")
    
    # Step 1: Pipeline start (like orchestrator line 76)
    run_id = "test_simple_20251102_130000"
    company_url = "https://example.com"
    genre = "Rock"
    
    print("STEP 1: Calling save_pipeline_start()...")
    result1 = save_pipeline_start(run_id, company_url, genre)
    print(f"  → Returned: {result1}\n")
    
    # Step 2: Update with summaries (like orchestrator line 136)
    print("STEP 2: Calling update_pipeline_progress() with summaries...")
    cv_summary = "Test CV summary with skills and experience"
    company_summary = "Test company doing AI and tech stuff"
    result2 = update_pipeline_progress(run_id, cv_summary=cv_summary, company_summary=company_summary)
    print(f"  → Returned: {result2}\n")
    
    # Step 3: Update with song data (like orchestrator line 154)
    print("STEP 3: Calling update_pipeline_progress() with song data...")
    song_data = {
        "song_title": "Test Song",
        "genre": "Rock",
        "bpm": 120,
        "mood": "Energetic",
        "scenes": [
            {"scene_num": 1, "lyrics": "Line 1"},
            {"scene_num": 2, "lyrics": "Line 2"},
            {"scene_num": 3, "lyrics": "Line 3"},
            {"scene_num": 4, "lyrics": "Line 4"},
            {"scene_num": 5, "lyrics": "Line 5"},
            {"scene_num": 6, "lyrics": "Line 6"}
        ]
    }
    output_dir = "/test/path/results/test_simple_20251102_130000"
    result3 = update_pipeline_progress(run_id, song_data=song_data, output_dir=output_dir)
    print(f"  → Returned: {result3}\n")
    
    # Step 4: Pipeline completion (like orchestrator line 284)
    print("STEP 4: Calling save_pipeline_completion()...")
    final_video_path = "/test/path/results/test_simple_20251102_130000/08_final_video.mp4"
    music_url = ""
    image_urls = [f"https://fal.media/image_{i}.jpg" for i in range(1, 7)]
    video_urls = [f"https://fal.media/video_{i}.mp4" for i in range(1, 7)]
    result4 = save_pipeline_completion(run_id, final_video_path, music_url, image_urls, video_urls)
    print(f"  → Returned: {result4}\n")
    
    print("="*80)
    if all([result1, result2, result3, result4]):
        print("✅ ALL DATABASE CALLS SUCCESSFUL!")
        print("\nCheck your Google Sheet - you should see:")
        print("  - Row with Run ID: test_simple_20251102_130000")
        print("  - Status: Completed")
        print("  - All song data and URLs filled in")
    else:
        print("⚠️  SOME DATABASE CALLS FAILED!")
        print(f"  save_pipeline_start: {result1}")
        print(f"  update summaries: {result2}")
        print(f"  update song data: {result3}")
        print(f"  save completion: {result4}")
    print("="*80)
    
    print("\nGoogle Sheet URL:")
    print("https://docs.google.com/spreadsheets/d/1ZBwSfDbNE9DA5YQ2LVGovLdhtkYzEwwmGiaLvE9E5QA/")

# Run the test
asyncio.run(test_pipeline())

