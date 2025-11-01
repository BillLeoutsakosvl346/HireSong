"""
Lyrics generation service using OpenAI Structured Outputs.
Generates song lyrics structured in 6 scenes for 30-second songs.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List


class Scene(BaseModel):
    scene_num: int
    time_range: str
    description: str
    lyrics: str
    musical_mood: str


class SongStructure(BaseModel):
    song_title: str
    genre: str
    bpm: int
    mood: str
    vocal_style: str
    instrumentation: str
    scenes: List[Scene]


def _ensure_openai_key():
    """Load .env and ensure OPENAI_API_KEY is available."""
    here = os.path.dirname(__file__)
    dotenv_path = os.path.abspath(os.path.join(here, '..', '..', '.env'))
    load_dotenv(dotenv_path)
    
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in backend/.env")
    return key


def generate_song_lyrics(cv_summary: str, company_summary: str) -> SongStructure:
    """
    Generate creative song lyrics based on CV and company summaries.
    
    Args:
        cv_summary: Summary of the candidate's CV with skills and experience
        company_summary: Summary of the company website with their values and products
        
    Returns:
        SongStructure object with complete song data including 6 scenes
    """
    _ensure_openai_key()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = """You are a creative and funny songwriter who creates catchy, memorable 30-second "hire me" pitch songs.

Your job is to create a complete song structure with:
- A catchy title
- Genre, BPM, mood, vocal style, and instrumentation
- 6 scenes of exactly 5 seconds each (0-5s, 5-10s, 10-15s, 15-20s, 20-25s, 25-30s)

CRITICAL LYRICS CONSTRAINTS:
- **THINK ABOUT THE GENRE YOU CHOOSE** - Different genres have different pacing!
- Adjust word count per scene based on the genre:
  * **Rap/Hip-Hop**: 15-20 words per scene (fast delivery)
  * **Pop/Rock**: 8-12 words per scene (moderate pace)
  * **Ballad/Slow**: 5-8 words per scene (slower, drawn-out)
  * **Electronic/Dance**: 6-10 words per scene (repetitive, punchy)
  * **Country/Folk**: 10-14 words per scene (storytelling pace)
- Match your lyrics to the natural rhythm and speed of your chosen genre
- Make lyrics rhyme when possible
- Be creative, funny, and memorable
- Weave in the candidate's best achievements and the company's keywords naturally

IMPORTANT: Try making it as ridiculus and funny as possible!"""

    user_prompt = f"""Create a catchy 30-second "hire me" song for this candidate applying to this company.

CANDIDATE SUMMARY:
{cv_summary}

COMPANY SUMMARY:
{company_summary}

Remember: Choose a genre first, then adjust the word count per scene to match that genre's natural pacing!"""

    print("🎵 Generating song lyrics with OpenAI GPT-5 (low reasoning)...")
    print(f"   Using structured outputs to ensure format...")
    
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=SongStructure,
            reasoning_effort="low",  # Low reasoning for creative, fast generation
            max_completion_tokens=20000  # Budget for the answer tokens
        )
        
        song = completion.choices[0].message.parsed
        
        print(f"✅ Generated song: '{song.song_title}'")
        print(f"   Genre: {song.genre} | BPM: {song.bpm}")
        
        return song
        
    except Exception as e:
        print(f"❌ Lyrics generation failed: {str(e)}")
        raise Exception(f"Failed to generate lyrics: {str(e)}")

