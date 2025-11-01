"""
Test for video assembly service.
Usage: python backend/tests/test_video_assembly.py

This test uses the generated files from test_run to assemble the final video.
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

from api.services.assembling_video import assemble_from_list

# Test
print("\nTesting video assembly...")

# Paths to test files from test_run
test_run_dir = os.path.join(BACKEND_DIR, "results", "test_run")

# Check if test_run directory exists
if not os.path.exists(test_run_dir):
    print(f"❌ Test run directory not found: {test_run_dir}")
    print("Please run: python backend/tests/test_full_pipeline.py")
    exit(1)

# Collect video paths
video_paths = []
for i in range(1, 7):
    video_path = os.path.join(test_run_dir, f"07_video_scene_{i}.mp4")
    if not os.path.exists(video_path):
        print(f"❌ Video {i} not found")
        exit(1)
    video_paths.append(video_path)

# Check music file
music_path = os.path.join(test_run_dir, "06_music.mp3")
if not os.path.exists(music_path):
    print(f"❌ Music not found")
    exit(1)

# Output path
output_path = os.path.join(test_run_dir, "08_final_video.mp4")
print(f"Output: {output_path}\n")

try:
    result = assemble_from_list(
        video_paths=video_paths,
        music_path=music_path,
        output_path=output_path
    )
    
    if os.path.exists(result):
        size_mb = os.path.getsize(result) / (1024 * 1024)
        print(f"\n🎉 Final video created: {size_mb:.2f} MB")
        print(f"Watch: {result}")
    else:
        print(f"❌ Failed to create output")
        exit(1)
        
except Exception as e:
    print(f"\n❌ Failed: {str(e)}")
    exit(1)

