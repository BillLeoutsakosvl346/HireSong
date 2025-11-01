"""
Scene planning service using OpenAI Structured Outputs.
Generates visual scene plans for 6 five-second video segments.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List


class SceneVisual(BaseModel):
    scene_num: int
    time_range: str
    scene_description: str
    image_prompt: str
    video_prompt: str


class ScenePlan(BaseModel):
    scenes: List[SceneVisual]


def _ensure_openai_key():
    """Load .env and ensure OPENAI_API_KEY is available."""
    here = os.path.dirname(__file__)
    dotenv_path = os.path.abspath(os.path.join(here, '..', '..', '.env'))
    load_dotenv(dotenv_path)
    
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in backend/.env")
    return key


def generate_scene_plan(cv_summary: str, company_summary: str, lyrics_data: dict) -> ScenePlan:
    """
    Generate visual scene plans for 6 five-second video segments.
    
    Args:
        cv_summary: Summary of the candidate's CV
        company_summary: Summary of the company website
        lyrics_data: Dictionary containing the song structure with lyrics for each scene
        
    Returns:
        ScenePlan object with 6 scenes, each containing visual descriptions and prompts
    """
    _ensure_openai_key()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = """You are a creative director for funny, viral TikTok-style pitch videos.

Your job is to create 6 hilarious, over-the-top visual scenes that match song lyrics for a "hire me" video.

IMPORTANT CONTEXT:
- A selfie of the candidate will be provided as a reference image to Nano Banana
- Nano Banana will TRANSFORM the person in the selfie based on your image prompt
- The video will then ANIMATE the Nano Banana generated image (not the original selfie)

For each 5-second scene, create:

1. **Scene Description**: What's happening visually (keep it funny and absurd!)

2. **Image Prompt** (for Nano Banana image editing):
   - This transforms the reference selfie into a completely new scene
   - **CRITICAL**: The person's FACE must stay the same, but EVERYTHING ELSE should change dramatically
   - **ALWAYS modify**: Background/setting, clothing/outfit, props, lighting, environment
   - Each scene should look completely different from the others
   - Be specific about the new setting, outfit, and props
   - Example: "Change background to a mountain peak covered in snow. Dress the person in a superhero cape and wizard hat. Add a glowing laptop in their hands. Add floating lines of code around them. Dramatic golden hour lighting."
   - DO NOT use specific names - just say "the person" or "the candidate"
   - Focus on COMPLETE transformations while keeping their face recognizable

3. **Video Prompt** (for Kling video animation):
   - This animates the Nano Banana generated image
   - Describe what movements/actions should happen
   - Keep it simple but funny
   - Should logically animate from the generated image
   - DO NOT use specific names - just say "the person" or "the candidate"
   - Example: "the person raises the laptop triumphantly while cape billows in the wind and code swirls around"

CRITICAL GUIDELINES:
- **MOST IMPORTANT**: Each scene MUST follow the song lyrics and be funny and ridiculous! 
  The visuals should match what's being sung and make people laugh!
- **PRESERVE THE FACE**: Nano Banana must keep the person's facial features identical
- **CHANGE EVERYTHING ELSE**: Every scene needs a different background, outfit, and setup
- NEVER use names (like "Alex", "Jordan") or company names (like "Google", "Anthropic")
- Always refer to "the person", "the candidate", "they", etc.
- Make it FUNNY and RIDICULOUS (think viral TikTok energy)
- Image prompt = describe the complete new scene with new background, new outfit, new props
- Video prompt = how to animate the transformed image (e.g. begging, dancing, celebrating)
- Both prompts must be COHERENT (video continues from the image)
- Each scene should be VISUALLY DISTINCT with unique settings and outfits

Examples of complete transformations:
- Background: Mountain peak → Clothing: Wizard robes → Props: Giant glowing keyboard
- Background: Outer space station → Clothing: Astronaut suit → Props: Floating code holograms
- Background: Underwater office → Clothing: Business suit with scuba gear → Props: Waterproof laptop
- Background: Desert with pyramids → Clothing: Explorer outfit → Props: Ancient scrolls of code
- Background: Rooftop at sunset → Clothing: Superhero cape → Props: Phone showing job offer
- Each should have different lighting: golden hour, neon lights, magical glow, etc.
You don't have to follow these exactly, just get an idea of what the vibe should be."""

    # Format the lyrics for context
    lyrics_context = "SONG LYRICS BY SCENE:\n"
    for scene in lyrics_data.get('scenes', []):
        lyrics_context += f"Scene {scene['scene_num']} ({scene['time_range']}): \"{scene['lyrics']}\"\n"
    
    user_prompt = f"""Create 6 hilarious visual scenes for this candidate's "hire me" video.

CANDIDATE SUMMARY:
{cv_summary}

COMPANY SUMMARY:
{company_summary}

{lyrics_context}

Make each scene visually funny and memorable while showcasing the candidate's fit for the role!"""

    print("🎬 Generating scene plans with OpenAI...")
    print(f"   Creating 6 visual scenes...")
    
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=ScenePlan,
            temperature=0.4 
        )
        
        scene_plan = completion.choices[0].message.parsed
        
        print(f"✅ Generated {len(scene_plan.scenes)} visual scenes")
        
        return scene_plan
        
    except Exception as e:
        print(f"❌ Scene planning failed: {str(e)}")
        raise Exception(f"Failed to generate scene plan: {str(e)}")

