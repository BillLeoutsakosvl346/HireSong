"""
Image generation service using Fal.ai Nano Banana Edit API.
Generates edited images based on a prompt and input image.
"""

import os
import fal_client
from dotenv import load_dotenv
from typing import Dict, Any, Optional


def _ensure_fal_key():
    """Load .env and ensure FAL_KEY is available."""
    # Load from backend/.env relative to this file
    here = os.path.dirname(__file__)
    dotenv_path = os.path.abspath(os.path.join(here, '..', '..', '.env'))
    load_dotenv(dotenv_path)
    
    key = os.getenv("FAL_KEY")
    if not key:
        raise ValueError("FAL_KEY not found. Please set it in backend/.env")
    return key


def generate_image_from_prompt(
    prompt: str,
    image_path: str,
    num_images: int = 1,
    output_format: str = "jpeg",
    aspect_ratio: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate an edited image using Nano Banana Edit API.
    
    Args:
        prompt: The editing instruction/prompt (e.g., "make the person wear sunglasses")
        image_path: Local file path to the input image
        num_images: Number of images to generate (default: 1)
        output_format: Output format - "jpeg", "png", or "webp" (default: "jpeg")
        aspect_ratio: Optional aspect ratio like "1:1", "16:9", etc.
    
    Returns:
        Dict containing:
            - images: List of generated image objects with 'url' field
            - description: Text description from the model
    
    Raises:
        Exception: If the API call fails
    """
    _ensure_fal_key()
    
    try:
        # Upload the local image file to Fal's storage
        print(f"Uploading image: {image_path}")
        image_url = fal_client.upload_file(image_path)
        print(f"Image uploaded: {image_url}")
        
        # Prepare arguments for the API
        arguments = {
            "prompt": prompt,
            "image_urls": [image_url],
            "num_images": num_images,
            "output_format": output_format,
        }
        
        # Add aspect ratio if provided
        if aspect_ratio:
            arguments["aspect_ratio"] = aspect_ratio
        
        print(f"Calling Nano Banana API with prompt: {prompt}")
        
        # Simple synchronous call - returns when done
        result = fal_client.run("fal-ai/nano-banana/edit", arguments=arguments)
        
        print(f"Image generation complete. Generated {len(result.get('images', []))} image(s)")
        return result
        
    except Exception as e:
        print(f"Error in image generation: {str(e)}")
        raise Exception(f"Failed to generate image with Nano Banana: {str(e)}")


def generate_image_from_url(
    prompt: str,
    image_url: str,
    num_images: int = 1,
    output_format: str = "jpeg",
    aspect_ratio: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate an edited image using Nano Banana Edit API from an existing URL.
    
    Args:
        prompt: The editing instruction/prompt
        image_url: URL of the input image (must be publicly accessible)
        num_images: Number of images to generate (default: 1)
        output_format: Output format - "jpeg", "png", or "webp" (default: "jpeg")
        aspect_ratio: Optional aspect ratio
    
    Returns:
        Dict containing:
            - images: List of generated image objects with 'url' field
            - description: Text description from the model
    """
    _ensure_fal_key()
    
    try:
        # Prepare arguments for the API
        arguments = {
            "prompt": prompt,
            "image_urls": [image_url],
            "num_images": num_images,
            "output_format": output_format,
        }
        
        # Add aspect ratio if provided
        if aspect_ratio:
            arguments["aspect_ratio"] = aspect_ratio
        
        print(f"Calling Nano Banana API with prompt: {prompt}")
        
        # Simple synchronous call - returns when done
        result = fal_client.run("fal-ai/nano-banana/edit", arguments=arguments)
        
        print(f"Image generation complete. Generated {len(result.get('images', []))} image(s)")
        return result
        
    except Exception as e:
        print(f"Error in image generation: {str(e)}")
        raise Exception(f"Failed to generate image with Nano Banana: {str(e)}")

