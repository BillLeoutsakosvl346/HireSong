"""
Full end-to-end pipeline test for HireSong.
Usage: python backend/tests/test_full_pipeline.py

This test runs the complete pipeline using test files.
"""

import sys
import os
import asyncio
import json

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from api.services.orchestrator import generate_hiresong_video


async def test_full_pipeline():
    """Run the complete HireSong pipeline."""
    
    print("\n" + "🎬" * 40)
    print("   HIRESONG FULL PIPELINE TEST")
    print("🎬" * 40 + "\n")
    
    # Paths to test files
    test_dir = os.path.join(BACKEND_DIR, "tests")
    selfie_path = os.path.join(test_dir, "test_images", "test_selfie.jpg")
    cv_path = os.path.join(test_dir, "test_files", "test_cv.pdf")
    company_url = "https://www.anthropic.com"
    
    # Verify test files exist
    print("Checking test files...")
    if not os.path.exists(selfie_path):
        print(f"❌ Selfie not found: {selfie_path}")
        return False
    print(f"✅ Selfie: {selfie_path}")
    
    if not os.path.exists(cv_path):
        print(f"❌ CV not found: {cv_path}")
        return False
    print(f"✅ CV: {cv_path}")
    
    print(f"✅ Company URL: {company_url}")
    
    # Create output directory for test
    output_dir = os.path.join(BACKEND_DIR, "results", "test_run")
    print(f"\n📂 Output directory: {output_dir}")
    
    print("\n" + "="*80)
    print("Starting full pipeline...")
    print("="*80)
    print("\n⏱️  This will take approximately 2-3 minutes...\n")
    
    try:
        # Run the pipeline
        results = await generate_hiresong_video(
            selfie_path=selfie_path,
            cv_path=cv_path,
            company_url=company_url,
            output_dir=output_dir
        )
        
        # Verify all outputs
        print("\n" + "="*80)
        print("VERIFYING OUTPUTS")
        print("="*80)
        
        checks = []
        
        # Check inputs
        checks.append(("Input selfie", results.get("input_selfie")))
        checks.append(("Input CV", results.get("input_cv")))
        
        # Check extractions
        checks.append(("CV text", results.get("cv_text")))
        checks.append(("Website text", results.get("website_text")))
        
        # Check summaries
        checks.append(("CV summary", results.get("cv_summary")))
        checks.append(("Company summary", results.get("company_summary")))
        
        # Check generated content
        checks.append(("Lyrics JSON", results.get("lyrics")))
        checks.append(("Scenes JSON", results.get("scenes")))
        checks.append(("Music MP3", results.get("music")))
        
        # Check images
        if "images" in results:
            for i, img_path in enumerate(results["images"], 1):
                checks.append((f"Image {i}/6", img_path))
        
        # Check videos
        if "videos" in results:
            for i, vid_path in enumerate(results["videos"], 1):
                checks.append((f"Video {i}/6", vid_path))
        
        # Check final video
        checks.append(("Final video", results.get("final_video")))
        
        # Print verification results
        all_passed = True
        for name, path in checks:
            if path and os.path.exists(path):
                size = os.path.getsize(path) / 1024  # KB
                print(f"✅ {name:20s} - {size:>8.1f} KB - {path}")
            else:
                print(f"❌ {name:20s} - MISSING")
                all_passed = False
        
        # Print summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        if all_passed:
            print("\n🎉 SUCCESS! Full pipeline completed successfully!")
            print(f"\nAll files saved to: {output_dir}")
            
            # Print manifest
            manifest_path = os.path.join(output_dir, "results_manifest.json")
            if os.path.exists(manifest_path):
                print(f"\n📋 Manifest: {manifest_path}")
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    print(f"\nGenerated {len(manifest.get('images', []))} images")
                    print(f"Generated {len(manifest.get('videos', []))} videos")
                    print(f"Generated 1 music track")
                    
                    if manifest.get('final_video') and os.path.exists(manifest['final_video']):
                        final_size = os.path.getsize(manifest['final_video']) / (1024 * 1024)
                        print(f"Generated final video: {final_size:.2f} MB")
                        print(f"\n🎬 Watch it here: {manifest['final_video']}")
            
            return True
        else:
            print("\n⚠️  Some outputs are missing. Check errors above.")
            return False
            
    except Exception as e:
        print("\n" + "="*80)
        print("❌ PIPELINE FAILED")
        print("="*80)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the async test."""
    result = asyncio.run(test_full_pipeline())
    exit(0 if result else 1)


if __name__ == "__main__":
    main()

