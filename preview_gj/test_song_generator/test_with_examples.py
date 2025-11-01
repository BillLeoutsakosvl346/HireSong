"""
Main test script for ElevenLabs Music API song generation.
Tests with pre-generated example songs (6-scene structured).
Generates complete 30-second songs in a single API call.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from elevenlabs_music_api import create_elevenlabs_client
from example_lyrics import ALL_EXAMPLES

# Create output directory if it doesn't exist
OUTPUT_DIR = Path(__file__).parent / "data" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


async def test_single_song(song_data: dict, song_index: int, save_audio: bool = False) -> dict:
    """
    Test generating a single 30-second song.
    
    Args:
        song_data: Dictionary with song structure (theme, title, scenes, etc.)
        song_index: Index of the song (for logging)
        save_audio: Whether to save audio to file
    
    Returns:
        Result dict with generation status and metadata
    """
    client = await create_elevenlabs_client()
    
    # Generate the complete 30-second song
    result = await client.generate_song(song_data)
    
    # Optionally save audio to file
    if save_audio and result.get('status') == 'success' and result.get('audio_data'):
        filename = f"song_{song_index + 1}_{song_data['theme']}.mp3"
        filepath = OUTPUT_DIR / filename
        filepath.write_bytes(result['audio_data'])
        result['saved_to'] = str(filepath)
        print(f"💾 Audio saved to: {filepath}")
    
    return result


async def test_all_songs(save_audio: bool = False):
    """
    Test all example songs sequentially.
    
    Args:
        save_audio: Whether to save generated audio files
    """
    print("=" * 90)
    print("🎵 HIRESONG ELEVENLABS MUSIC API TEST - 30 SECOND GENERATION")
    print("=" * 90)
    print(f"Starting at: {datetime.now().isoformat()}\n")
    print(f"Output Directory: {OUTPUT_DIR}\n")
    print(f"Mode: {'Save audio files' if save_audio else 'Test only (no audio files saved)'}\n")
    
    results = []
    
    for idx, song_data in enumerate(ALL_EXAMPLES):
        print(f"\n{'='*90}")
        print(f"SONG {idx + 1}/{len(ALL_EXAMPLES)}: {song_data['song_title'].upper()}")
        print(f"{'='*90}")
        print(f"🎼 Musical Info:")
        print(f"   Theme:           {song_data['theme']}")
        print(f"   Genre:           {song_data['genre']}")
        print(f"   BPM:             {song_data['bpm']}")
        print(f"   Mood:            {song_data['mood']}")
        print(f"   Vocal Style:     {song_data['vocal_style']}")
        print(f"   Instrumentation: {song_data['instrumentation']}")
        print(f"   Scenes:          {len(song_data['scenes'])} (5 seconds each)")
        print()
        
        try:
            result = await test_single_song(song_data, idx, save_audio=save_audio)
            
            if result.get('status') == 'success':
                results.append({
                    "song_index": idx + 1,
                    "theme": song_data["theme"],
                    "title": song_data["song_title"],
                    "status": "success",
                    "data": result
                })
                
                # Print result summary
                print(f"✨ SUCCESS!")
                print(f"\n📊 Result Summary:")
                print(f"   Duration: {result.get('duration_seconds', 0)} seconds")
                print(f"   Audio Data Size: {len(result.get('audio_data', b'')) / 1024:.2f} KB")
                print(f"   Metadata: {result.get('metadata', {})}")
                
                if result.get('saved_to'):
                    print(f"   Saved to: {result['saved_to']}")
            else:
                results.append({
                    "song_index": idx + 1,
                    "theme": song_data["theme"],
                    "title": song_data["song_title"],
                    "status": "failed",
                    "error": result.get('error', 'Unknown error')
                })
                print(f"\n❌ Generation failed")
                print(f"   Error: {result.get('error', 'No error message')}")
        
        except Exception as e:
            print(f"\n❌ Exception during song generation: {e}")
            results.append({
                "song_index": idx + 1,
                "theme": song_data["theme"],
                "title": song_data["song_title"],
                "status": "error",
                "error": str(e)
            })
        
        # Delay between songs to avoid rate limits
        if idx < len(ALL_EXAMPLES) - 1:
            print(f"\n⏳ Waiting 10 seconds before next song...")
            await asyncio.sleep(10)
    
    # Print final report
    print(f"\n\n{'='*90}")
    print("📋 FINAL TEST REPORT")
    print(f"{'='*90}\n")
    
    success_count = 0
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{status_icon} Song {result['song_index']}: {result['title']}")
        print(f"   Theme:  {result['theme']}")
        print(f"   Status: {result['status']}")
        if result["status"] == "success":
            data = result['data']
            print(f"   Duration: {data.get('duration_seconds', 0)} seconds")
            print(f"   Audio Size: {len(data.get('audio_data', b'')) / 1024:.2f} KB")
            if data.get('saved_to'):
                print(f"   Saved: {data['saved_to']}")
            success_count += 1
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        print()
    
    # Summary statistics
    print(f"\n{'='*90}")
    print(f"📈 SUMMARY")
    print(f"{'='*90}")
    print(f"Total Songs: {len(results)}")
    print(f"Successful: {success_count} ✅")
    print(f"Failed: {len(results) - success_count} ❌")
    print(f"Success Rate: {(success_count / len(results) * 100):.1f}%")
    print(f"Output Directory: {OUTPUT_DIR}")
    print()
    
    # Save results to file (without audio_data for readability)
    results_clean = []
    for r in results:
        r_clean = r.copy()
        if 'data' in r_clean and 'audio_data' in r_clean['data']:
            r_clean['data'] = {k: v for k, v in r_clean['data'].items() if k != 'audio_data'}
            r_clean['data']['audio_size_kb'] = len(r['data']['audio_data']) / 1024
        results_clean.append(r_clean)
    
    results_file = OUTPUT_DIR / 'test_results.json'
    with open(results_file, 'w') as f:
        json.dump(results_clean, f, indent=2)
    
    print(f"✅ Results saved to: {results_file}")
    print(f"Completed at: {datetime.now().isoformat()}\n")


async def test_single_example(song_index: int = 0, save_audio: bool = True):
    """
    Quick test with a single example song (useful for debugging).
    
    Args:
        song_index: Index of example to test (0, 1, or 2)
        save_audio: Whether to save the generated audio
    """
    if song_index >= len(ALL_EXAMPLES):
        print(f"❌ Invalid song index. Choose 0-{len(ALL_EXAMPLES)-1}")
        return
    
    print("=" * 90)
    song_data = ALL_EXAMPLES[song_index]
    print(f"🎵 TESTING SINGLE SONG: {song_data['song_title'].upper()}")
    print("=" * 90)
    print(f"Output Directory: {OUTPUT_DIR}\n")
    print(f"🎼 Musical Info:")
    print(f"   Theme:           {song_data['theme']}")
    print(f"   Genre:           {song_data['genre']}")
    print(f"   BPM:             {song_data['bpm']}")
    print(f"   Mood:            {song_data['mood']}")
    print(f"   Vocal Style:     {song_data['vocal_style']}")
    print(f"   Instrumentation: {song_data['instrumentation']}")
    print()
    
    result = await test_single_song(song_data, song_index, save_audio=save_audio)
    
    if result.get('status') == 'success':
        print(f"\n✅ Success!")
        print(f"Duration: {result.get('duration_seconds', 0)} seconds")
        print(f"Audio Size: {len(result.get('audio_data', b'')) / 1024:.2f} KB")
        if result.get('saved_to'):
            print(f"Saved to: {result['saved_to']}")
    else:
        print(f"\n❌ Failed to generate song")
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    # Run all test songs and save audio
    asyncio.run(test_all_songs(save_audio=True))
    
    # Or test a single song (uncomment to use):
    # asyncio.run(test_single_example(0, save_audio=True))
