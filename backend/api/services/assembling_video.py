"""
Video assembly service using MoviePy v2.
Combines 6 five-second videos with a 30-second music track.
"""

import os
import sys
import warnings
from contextlib import contextmanager
from io import StringIO
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx.AudioLoop import AudioLoop

# Suppress MoviePy/ffmpeg verbose output
warnings.filterwarnings('ignore')


@contextmanager
def suppress_output():
    """Context manager to suppress stdout and stderr."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def assemble_final_video(
    video_1: str,
    video_2: str,
    video_3: str,
    video_4: str,
    video_5: str,
    video_6: str,
    music_path: str,
    output_path: str
) -> str:
    """
    Assemble 6 five-second videos with music into a final 30-second video.
    
    Args:
        video_1 to video_6: Paths to the 6 video files (in order)
        music_path: Path to the music file (30 seconds)
        output_path: Path where the final video will be saved
        
    Returns:
        Path to the assembled video file
    """
    
    print("🎬 Assembling final video...")
    
    video_clips = []
    audio = None
    final_clip = None
    music = None
    
    try:
        # Load all video clips and force each to exactly 5.0s
        video_paths = [video_1, video_2, video_3, video_4, video_5, video_6]
        
        for i, video_path in enumerate(video_paths, 1):
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video {i} not found: {video_path}")
            
            with suppress_output():
                clip = VideoFileClip(video_path).subclipped(0, 5)  # Force exactly 5s
            video_clips.append(clip)
        
        # Concatenate all video clips (6 × 5s = 30s exactly)
        final_clip = concatenate_videoclips(video_clips, method="compose")
        
        # Load music and force to exactly 30s
        if not os.path.exists(music_path):
            raise FileNotFoundError(f"Music file not found: {music_path}")
        
        with suppress_output():
            audio = AudioFileClip(music_path)
            
            # Make music exactly 30s (trim if longer, loop if shorter)
            if audio.duration >= 30:
                music = audio.subclipped(0, 30)
            else:
                music = audio.with_effects([AudioLoop(duration=30)])
        
        # Attach audio (v2 method) and pin duration to 30s
        final_clip = final_clip.with_audio(music).with_duration(30)
        
        # Write the final video
        print("  Writing video...")
        
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=24,
            preset='medium',
            threads=4,
            logger=None  # Suppress moviepy's verbose output
        )
        
        # Verify output
        if not os.path.exists(output_path):
            raise Exception("Failed to create output video")
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        print(f"✅ Video assembled: {file_size:.2f} MB")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Assembly failed: {str(e)}")
        raise Exception(f"Failed to assemble video: {str(e)}")
        
    finally:
        # Always clean up resources
        for clip in video_clips:
            try:
                clip.close()
            except:
                pass
        if audio:
            try:
                audio.close()
            except:
                pass
        if music:
            try:
                music.close()
            except:
                pass
        if final_clip:
            try:
                final_clip.close()
            except:
                pass


def assemble_from_list(
    video_paths: list,
    music_path: str,
    output_path: str
) -> str:
    """
    Convenience function to assemble videos from a list.
    
    Args:
        video_paths: List of 6 video file paths (in order)
        music_path: Path to the music file
        output_path: Path where the final video will be saved
        
    Returns:
        Path to the assembled video file
    """
    
    if len(video_paths) != 6:
        raise ValueError(f"Expected 6 videos, got {len(video_paths)}")
    
    return assemble_final_video(
        video_paths[0],
        video_paths[1],
        video_paths[2],
        video_paths[3],
        video_paths[4],
        video_paths[5],
        music_path,
        output_path
    )

