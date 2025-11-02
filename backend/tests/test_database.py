"""
Test Google Sheets database integration.
Usage: python backend/tests/test_database.py
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.database import (
    initialize_sheet,
    save_pipeline_start,
    update_pipeline_progress,
    save_pipeline_completion,
    save_pipeline_error,
    get_all_runs,
    get_run_by_id
)

def test_database():
    print("="*80)
    print("TESTING GOOGLE SHEETS DATABASE")
    print("="*80)
    
    # Test 1: Initialize sheet
    print("\n[1] Testing sheet initialization...")
    success = initialize_sheet()
    if success:
        print("✅ Sheet initialized successfully")
    else:
        print("❌ Sheet initialization failed")
        return
    
    # Test 2: Save pipeline start
    print("\n[2] Testing save_pipeline_start()...")
    run_id = "test_20251102_120000"
    company_url = "https://anthropic.com"
    genre = "Pop"
    
    success = save_pipeline_start(run_id, company_url, genre)
    if success:
        print(f"✅ Saved pipeline start (Run ID: {run_id})")
    else:
        print("❌ Failed to save pipeline start")
        return
    
    # Test 3: Update with summaries
    print("\n[3] Testing update_pipeline_progress() with summaries...")
    cv_summary = "Software Engineer with 5 years experience in Python, React, and ML. Previously at Google and OpenAI."
    company_summary = "Anthropic is an AI safety company building Claude, focusing on helpful, harmless, and honest AI."
    
    success = update_pipeline_progress(
        run_id,
        cv_summary=cv_summary,
        company_summary=company_summary
    )
    if success:
        print("✅ Updated with CV and company summaries")
    else:
        print("❌ Failed to update summaries")
    
    # Test 4: Update with song data
    print("\n[4] Testing update_pipeline_progress() with song data...")
    song_data = {
        "song_title": "Code My Way to Anthropic",
        "genre": "Pop",
        "bpm": 120,
        "mood": "Upbeat and confident",
        "scenes": [
            {"scene_num": 1, "lyrics": "I've been coding through the night"},
            {"scene_num": 2, "lyrics": "Building AI that feels so right"},
            {"scene_num": 3, "lyrics": "Safety first in every line"},
            {"scene_num": 4, "lyrics": "Claude's my dream, so I'll shine"},
            {"scene_num": 5, "lyrics": "Anthropic is where I belong"},
            {"scene_num": 6, "lyrics": "Hire me and we'll make it strong"}
        ]
    }
    
    output_dir = "/path/to/results/test_20251102_120000"
    
    success = update_pipeline_progress(
        run_id,
        song_data=song_data,
        output_dir=output_dir
    )
    if success:
        print("✅ Updated with song data and output directory")
    else:
        print("❌ Failed to update song data")
    
    # Test 5: Save completion
    print("\n[5] Testing save_pipeline_completion()...")
    final_video_path = "/path/to/results/test_20251102_120000/08_final_video.mp4"
    music_url = "https://storage.example.com/music/test_song.mp3"
    image_urls = [
        "https://v3.fal.media/files/test/image_1.jpg",
        "https://v3.fal.media/files/test/image_2.jpg",
        "https://v3.fal.media/files/test/image_3.jpg",
        "https://v3.fal.media/files/test/image_4.jpg",
        "https://v3.fal.media/files/test/image_5.jpg",
        "https://v3.fal.media/files/test/image_6.jpg"
    ]
    video_urls = [
        "https://v3.fal.media/files/test/video_1.mp4",
        "https://v3.fal.media/files/test/video_2.mp4",
        "https://v3.fal.media/files/test/video_3.mp4",
        "https://v3.fal.media/files/test/video_4.mp4",
        "https://v3.fal.media/files/test/video_5.mp4",
        "https://v3.fal.media/files/test/video_6.mp4"
    ]
    
    success = save_pipeline_completion(
        run_id,
        final_video_path=final_video_path,
        music_url=music_url,
        image_urls=image_urls,
        video_urls=video_urls,
        status="Completed"
    )
    if success:
        print("✅ Saved pipeline completion")
    else:
        print("❌ Failed to save completion")
    
    # Test 6: Get all runs
    print("\n[6] Testing get_all_runs()...")
    runs = get_all_runs()
    if runs:
        print(f"✅ Retrieved {len(runs)} run(s) from database")
        print("\nRecent runs:")
        for run in runs[-3:]:  # Show last 3 runs
            print(f"  - {run.get('Timestamp', 'N/A')}: {run.get('Company URL', 'N/A')} [{run.get('Status', 'N/A')}]")
    else:
        print("⚠️  No runs found or failed to retrieve")
    
    # Test 7: Get specific run
    print(f"\n[7] Testing get_run_by_id() for {run_id}...")
    run = get_run_by_id(run_id)
    if run:
        print("✅ Retrieved run successfully")
        print(f"\n  Run Details:")
        print(f"  - Song Title: {run.get('Song Title', 'N/A')}")
        print(f"  - Genre: {run.get('Song Genre', 'N/A')}")
        print(f"  - BPM: {run.get('BPM', 'N/A')}")
        print(f"  - Status: {run.get('Status', 'N/A')}")
    else:
        print("❌ Failed to retrieve run")
    
    # Test 8: Test error saving
    print("\n[8] Testing save_pipeline_error()...")
    error_run_id = "test_error_20251102_120100"
    save_pipeline_start(error_run_id, "https://example.com", "Rock")
    
    success = save_pipeline_error(error_run_id, "Test error: Something went wrong!")
    if success:
        print("✅ Saved error successfully")
    else:
        print("❌ Failed to save error")
    
    print("\n" + "="*80)
    print("DATABASE TEST COMPLETED!")
    print("="*80)
    print("\nCheck your Google Sheet:")
    print("https://docs.google.com/spreadsheets/d/1ZBwSfDbNE9DA5YQ2LVGovLdhtkYzEwwmGiaLvE9E5QA/")

if __name__ == "__main__":
    test_database()

