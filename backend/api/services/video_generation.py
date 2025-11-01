"""
Video generation service using Fal.ai Kling 2.5 Pro.
Generates videos from images and prompts using image-to-video.
"""

import os
import fal_client
from dotenv import load_dotenv
from typing import Dict, Any, Optional


def _ensure_fal_key():
    """Load .env and ensure FAL_KEY is available."""
    here = os.path.dirname(__file__)
    dotenv_path = os.path.abspath(os.path.join(here, '..', '..', '.env'))
    load_dotenv(dotenv_path)
    
    key = os.getenv("FAL_KEY")
    if not key:
        raise ValueError("FAL_KEY not found. Please set it in backend/.env")
    return key


def generate_video_from_image(
    prompt: str,
    image_path: str,
    duration: str = "5",
    aspect_ratio: str = "16:9",
    negative_prompt: Optional[str] = None,
    cfg_scale: float = 0.5
) -> Dict[str, Any]:
    """
    Generate a video from an image using Kling 2.5 Pro.
    
    Args:
        prompt: Description of the desired video motion/scene
        image_path: Local path to the input image
        duration: Video duration - "5" or "10" seconds (default: "5")
        aspect_ratio: "16:9", "9:16", or "1:1" (default: "16:9")
        negative_prompt: What to avoid in the video
        cfg_scale: Configuration scale (default: 0.5)
        
    Returns:
        Dict containing:
            - video: Dict with 'url' field pointing to generated MP4
    """
    _ensure_fal_key()
    
    try:
        # Upload the local image file to Fal's storage
        print(f"Uploading image: {image_path}")
        image_url = fal_client.upload_file(image_path)
        print(f"Image uploaded: {image_url}")
        
        # Prepare arguments
        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "cfg_scale": cfg_scale,
        }
        
        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        else:
            arguments["negative_prompt"] = "blur, distort, and low quality"
        
        print(f"Generating video with Kling 2.5 Pro...")
        print(f"  Prompt: '{prompt}'")
        print(f"  Duration: {duration}s")
        print(f"  This may take 30-60 seconds...\n")
        
        # Call the API
        result = fal_client.run(
            "fal-ai/kling-video/v2.5-turbo/pro/image-to-video",
            arguments=arguments
        )
        
        print(f"✅ Video generation complete!")
        return result
        
    except Exception as e:
        print(f"Error in video generation: {str(e)}")
        raise Exception(f"Failed to generate video with Kling: {str(e)}")


def generate_video_from_url(
    prompt: str,
    image_url: str,
    duration: str = "5",
    aspect_ratio: str = "16:9",
    negative_prompt: Optional[str] = None,
    cfg_scale: float = 0.5
) -> Dict[str, Any]:
    """
    Generate a video from an image URL using Kling 2.5 Pro.
    
    Args:
        prompt: Description of the desired video motion/scene
        image_url: Public URL of the input image
        duration: Video duration - "5" or "10" seconds (default: "5")
        aspect_ratio: "16:9", "9:16", or "1:1" (default: "16:9")
        negative_prompt: What to avoid in the video
        cfg_scale: Configuration scale (default: 0.5)
        
    Returns:
        Dict containing:
            - video: Dict with 'url' field pointing to generated MP4
    """
    _ensure_fal_key()
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "cfg_scale": cfg_scale,
        }
        
        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        else:
            arguments["negative_prompt"] = "blur, distort, and low quality"
        
        print(f"Generating video with Kling 2.5 Pro...")
        print(f"  Prompt: '{prompt}'")
        print(f"  Duration: {duration}s")
        print(f"  This may take 30-60 seconds...\n")
        
        # Call the API
        result = fal_client.run(
            "fal-ai/kling-video/v2.5-turbo/pro/image-to-video",
            arguments=arguments
        )
        
        print(f"✅ Video generation complete!")
        return result
        
    except Exception as e:
        print(f"Error in video generation: {str(e)}")
        raise Exception(f"Failed to generate video with Kling: {str(e)}")

