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
print("Testing video assembly with MoviePy...")
print("\n" + "="*80)
print("VIDEO ASSEMBLY TEST")
print("="*80)

# Paths to test files from test_run
test_run_dir = os.path.join(BACKEND_DIR, "results", "test_run")

# Check if test_run directory exists
if not os.path.exists(test_run_dir):
    print(f"\n❌ Test run directory not found: {test_run_dir}")
    print("\nPlease run the full pipeline test first:")
    print("  python backend/tests/test_full_pipeline.py")
    exit(1)

print(f"\n📂 Using files from: {test_run_dir}")

# Collect video paths
video_paths = []
for i in range(1, 7):
    video_path = os.path.join(test_run_dir, f"07_video_scene_{i}.mp4")
    if not os.path.exists(video_path):
        print(f"\n❌ Video {i} not found: {video_path}")
        print("\nPlease run the full pipeline test first to generate all videos.")
        exit(1)
    video_paths.append(video_path)
    
    # Show video info
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"  ✅ Video {i}/6 - {size_mb:.2f} MB - {video_path}")

# Check music file
music_path = os.path.join(test_run_dir, "06_music.mp3")
if not os.path.exists(music_path):
    print(f"\n❌ Music not found: {music_path}")
    print("\nPlease run the full pipeline test first to generate music.")
    exit(1)

music_size_mb = os.path.getsize(music_path) / (1024 * 1024)
print(f"  ✅ Music - {music_size_mb:.2f} MB - {music_path}")

# Output path
output_path = os.path.join(test_run_dir, "08_final_video.mp4")
print(f"\n📹 Output will be saved to: {output_path}")

# Assemble the video
print("\n" + "="*80)
print("ASSEMBLING VIDEO")
print("="*80 + "\n")

try:
    result = assemble_from_list(
        video_paths=video_paths,
        music_path=music_path,
        output_path=output_path
    )
    
    print("\n" + "="*80)
    print("TEST RESULT")
    print("="*80)
    
    if os.path.exists(result):
        size_mb = os.path.getsize(result) / (1024 * 1024)
        print(f"\n✅ SUCCESS!")
        print(f"\nFinal video created:")
        print(f"  Path: {result}")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"\n🎉 You can now watch the final HireSong video!")
        print(f"\nTo play it:")
        print(f"  Open: {result}")
    else:
        print(f"\n❌ FAILED: Output file not created")
        exit(1)
        
except Exception as e:
    print("\n" + "="*80)
    print("❌ TEST FAILED")
    print("="*80)
    print(f"\nError: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

