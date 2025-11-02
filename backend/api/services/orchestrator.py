"""
Orchestrator for the full HireSong pipeline.
Coordinates all services with async optimization.
"""

import os
import asyncio
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Import all services
from .text_extraction import extract_text_from_pdf
from .website_scraper import scrape_website
from .summarization import summarize_cv, summarize_company_website
from .lyrics_generation import generate_song_lyrics
from .scene_planning import generate_scene_plan
from .image_generation import generate_image_from_prompt
from .video_generation import generate_video_from_url
from .music_generation import generate_music
from .assembling_video import assemble_from_list
from .database import (
    save_pipeline_start,
    update_pipeline_progress,
    save_pipeline_completion,
    save_pipeline_error
)


async def run_sync_in_thread(func, *args, **kwargs):
    """Run a synchronous function in a thread pool."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def generate_hiresong_video(
    selfie_path: str,
    cv_path: str,
    company_url: str,
    output_dir: str = None,
    preferred_genre: str = None
) -> Dict[str, Any]:
    """
    Orchestrate the full HireSong pipeline with async optimization.
    
    Args:
        selfie_path: Path to candidate's selfie image
        cv_path: Path to candidate's CV PDF
        company_url: URL of target company website
        output_dir: Directory to save all outputs (defaults to backend/results/{timestamp})
        preferred_genre: Optional user-selected music genre
        
    Returns:
        Dictionary with paths to all generated files
    """
    
    # Create output directory
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results', timestamp)
    else:
        # Extract timestamp from output_dir if provided
        timestamp = os.path.basename(output_dir)
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("🎵 HIRESONG PIPELINE STARTED")
    print("="*80)
    print(f"Output directory: {output_dir}\n")
    
    # Save pipeline start to database
    run_id = timestamp
    print(f"\n🔍 DEBUG: About to call save_pipeline_start('{run_id}', '{company_url}', '{preferred_genre}')")
    try:
        save_pipeline_start(run_id, company_url, preferred_genre)
        print("🔍 DEBUG: save_pipeline_start() call completed")
    except Exception as e:
        print(f"🔍 DEBUG: save_pipeline_start() raised exception: {e}")
        import traceback
        traceback.print_exc()
    
    results = {
        "output_dir": output_dir,
        "timestamp": datetime.now().isoformat(),
        "run_id": run_id
    }
    
    # Copy input files to results
    print("📂 Copying input files...")
    selfie_copy = os.path.join(output_dir, "00_input_selfie.jpg")
    cv_copy = os.path.join(output_dir, "00_input_cv.pdf")
    shutil.copy(selfie_path, selfie_copy)
    shutil.copy(cv_path, cv_copy)
    results["input_selfie"] = selfie_copy
    results["input_cv"] = cv_copy
    results["input_company_url"] = company_url
    
    try:
        # STEP 1 & 2: Extract CV and scrape website in parallel
        print("\n" + "-"*80)
        print("STEP 1 & 2: Extracting CV and scraping website (parallel)")
        print("-"*80)
        
        cv_text, website_text = await asyncio.gather(
            run_sync_in_thread(extract_text_from_pdf, cv_path),
            run_sync_in_thread(scrape_website, company_url)
        )
        
        # Save extracted texts
        cv_text_path = os.path.join(output_dir, "01_cv_text.txt")
        website_text_path = os.path.join(output_dir, "01_website_text.txt")
        with open(cv_text_path, 'w', encoding='utf-8') as f:
            f.write(cv_text)
        with open(website_text_path, 'w', encoding='utf-8') as f:
            f.write(website_text)
        results["cv_text"] = cv_text_path
        results["website_text"] = website_text_path
        
        # STEP 3: Summarize both in parallel
        print("\n" + "-"*80)
        print("STEP 3: Summarizing CV and company (parallel)")
        print("-"*80)
        
        cv_summary, company_summary = await asyncio.gather(
            run_sync_in_thread(summarize_cv, cv_text),
            run_sync_in_thread(summarize_company_website, website_text)
        )
        
        # Save summaries
        cv_summary_path = os.path.join(output_dir, "02_cv_summary.txt")
        company_summary_path = os.path.join(output_dir, "02_company_summary.txt")
        with open(cv_summary_path, 'w', encoding='utf-8') as f:
            f.write(cv_summary)
        with open(company_summary_path, 'w', encoding='utf-8') as f:
            f.write(company_summary)
        results["cv_summary"] = cv_summary_path
        results["company_summary"] = company_summary_path
        
        # Update database with summaries
        print(f"\n🔍 DEBUG: About to call update_pipeline_progress (summaries)")
        try:
            update_pipeline_progress(run_id, cv_summary=cv_summary, company_summary=company_summary)
            print("🔍 DEBUG: update_pipeline_progress (summaries) completed")
        except Exception as e:
            print(f"🔍 DEBUG: update_pipeline_progress (summaries) raised exception: {e}")
    
        # STEP 4: Generate lyrics
        print("\n" + "-"*80)
        print("STEP 4: Generating song lyrics")
        print("-"*80)
        
        song_structure = await run_sync_in_thread(
            generate_song_lyrics, cv_summary, company_summary, preferred_genre
        )
        
        # Save lyrics
        lyrics_path = os.path.join(output_dir, "03_lyrics.json")
        with open(lyrics_path, 'w', encoding='utf-8') as f:
            json.dump(song_structure.model_dump(), f, indent=2)
        results["lyrics"] = lyrics_path
        
        # Update database with song data and output directory
        print(f"\n🔍 DEBUG: About to call update_pipeline_progress (song data)")
        try:
            update_pipeline_progress(
                run_id,
                song_data=song_structure.model_dump(),
                output_dir=output_dir
            )
            print("🔍 DEBUG: update_pipeline_progress (song data) completed")
        except Exception as e:
            print(f"🔍 DEBUG: update_pipeline_progress (song data) raised exception: {e}")
        
        # STEP 5: Generate scene plan
        print("\n" + "-"*80)
        print("STEP 5: Planning visual scenes")
        print("-"*80)
        
        scene_plan = await run_sync_in_thread(
            generate_scene_plan, cv_summary, company_summary, song_structure.model_dump()
        )
        
        # Save scene plan
        scenes_path = os.path.join(output_dir, "04_scenes.json")
        with open(scenes_path, 'w', encoding='utf-8') as f:
            json.dump(scene_plan.model_dump(), f, indent=2)
        results["scenes"] = scenes_path
    
        # STEP 6: Generate images (parallel) and STEP 8: Generate music (parallel)
        print("\n" + "-"*80)
        print("STEP 6 & 8: Generating 6 images + music (parallel)")
        print("-"*80)
        
        async def generate_single_image(scene_num: int, image_prompt: str):
            """Generate a single image."""
            print(f"  Generating image {scene_num}/6...")
            result = await run_sync_in_thread(
                generate_image_from_prompt, image_prompt, selfie_path
            )
            
            # Download and save image
            import requests
            image_url = result['images'][0]['url']
            response = requests.get(image_url)
            image_path = os.path.join(output_dir, f"05_image_scene_{scene_num}.jpg")
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            return {
                "scene_num": scene_num,
                "image_path": image_path,
                "image_url": image_url
            }
        
        # Generate all images and music in parallel
        image_tasks = [
            generate_single_image(scene.scene_num, scene.image_prompt)
            for scene in scene_plan.scenes
        ]
        music_task = run_sync_in_thread(generate_music, song_structure.model_dump())
        
        images_results, music_result = await asyncio.gather(
            asyncio.gather(*image_tasks),
            music_task
        )
        
        # Save music
        music_path = os.path.join(output_dir, "06_music.mp3")
        with open(music_path, 'wb') as f:
            f.write(music_result['audio_data'])
        results["music"] = music_path
        results["images"] = [img["image_path"] for img in images_results]
    
        # STEP 7: Generate videos (parallel)
        print("\n" + "-"*80)
        print("STEP 7: Generating 6 videos (parallel)")
        print("-"*80)
        
        async def generate_single_video(scene_num: int, image_url: str, video_prompt: str):
            """Generate a single video."""
            print(f"  Generating video {scene_num}/6...")
            result = await run_sync_in_thread(
                generate_video_from_url, video_prompt, image_url, duration="5"
            )
            
            # Download and save video
            import requests
            video_url = result['video']['url']
            response = requests.get(video_url)
            video_path = os.path.join(output_dir, f"07_video_scene_{scene_num}.mp4")
            with open(video_path, 'wb') as f:
                f.write(response.content)
            
            return {
                "scene_num": scene_num,
                "video_path": video_path,
                "video_url": video_url
            }
        
        video_tasks = [
            generate_single_video(
                img["scene_num"],
                img["image_url"],
                scene_plan.scenes[i].video_prompt
            )
            for i, img in enumerate(images_results)
        ]
        
        videos_results = await asyncio.gather(*video_tasks)
        results["videos"] = [vid["video_path"] for vid in videos_results]
        
        # STEP 9: Edit final video (combine all)
        print("\n" + "-"*80)
        print("STEP 9: Assembling final video")
        print("-"*80)
        
        final_video_path = os.path.join(output_dir, "08_final_video.mp4")
        
        # Extract lyrics from song structure for overlay
        # NOTE: Lyrics overlay disabled for now due to font compatibility issues
        # lyrics_list = [scene.lyrics for scene in song_structure.scenes]
        
        await run_sync_in_thread(
            assemble_from_list,
            [vid["video_path"] for vid in videos_results],
            music_path,
            final_video_path,
            None  # No lyrics overlay for now
        )
    
        results["final_video"] = final_video_path
        
        # Extract URLs for database
        image_urls = [img["image_url"] for img in images_results]
        video_urls = [vid["video_url"] for vid in videos_results]
        
        # Save completion to database
        # Note: music_url is empty string since ElevenLabs returns audio data, not a URL
        print(f"\n🔍 DEBUG: About to call save_pipeline_completion()")
        try:
            save_pipeline_completion(
                run_id,
                final_video_path=final_video_path,
                music_url="",  # Not uploaded to external storage
                image_urls=image_urls,
                video_urls=video_urls,
                status="Completed"
            )
            print("🔍 DEBUG: save_pipeline_completion() completed")
        except Exception as e:
            print(f"🔍 DEBUG: save_pipeline_completion() raised exception: {e}")
        
        # Save results manifest
        manifest_path = os.path.join(output_dir, "results_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "="*80)
        print("🎉 HIRESONG PIPELINE COMPLETED!")
        print("="*80)
        print(f"\nAll files saved to: {output_dir}")
        print(f"Manifest: {manifest_path}\n")
        
        return results
    
    except Exception as e:
        # Save error to database
        error_message = str(e)
        print(f"\n❌ Pipeline failed: {error_message}")
        
        # Try to save any URLs that were generated before the error
        print("🔍 DEBUG: Attempting to save partial results before error...")
        try:
            # Check if we got far enough to generate images and videos
            try:
                # These will raise NameError if not defined
                test_images = images_results
                test_videos = videos_results
                
                image_urls = [img["image_url"] for img in images_results]
                video_urls = [vid["video_url"] for vid in videos_results]
                print(f"🔍 DEBUG: Saving {len(image_urls)} image URLs and {len(video_urls)} video URLs")
                
                # Save partial completion with error status
                save_pipeline_completion(
                    run_id,
                    final_video_path="",  # No final video since it failed
                    music_url="",
                    image_urls=image_urls,
                    video_urls=video_urls,
                    status=f"Failed: {error_message[:100]}"
                )
            except NameError:
                print("🔍 DEBUG: Images/videos not generated yet, saving error only")
                save_pipeline_error(run_id, error_message)
        except Exception as db_error:
            print(f"⚠️  Failed to save error details: {db_error}")
            try:
                save_pipeline_error(run_id, error_message)
            except:
                pass
        
        # Re-raise the exception
        raise

