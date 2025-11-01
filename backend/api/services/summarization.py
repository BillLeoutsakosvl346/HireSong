"""
Summarization service using OpenAI.
Summarizes CV text into a clean, structured outline.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv


def _ensure_openai_key():
    """Load .env and ensure OPENAI_API_KEY is available."""
    here = os.path.dirname(__file__)
    dotenv_path = os.path.abspath(os.path.join(here, '..', '..', '.env'))
    load_dotenv(dotenv_path)
    
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in backend/.env")
    return key


def summarize_cv(raw_cv_text: str) -> str:
    """
    Summarize raw CV text into a clean, structured outline.
    
    Args:
        raw_cv_text: The full text extracted from the CV file
        
    Returns:
        A clean text summary outlining all experiences and qualifications
    """
    _ensure_openai_key()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = """You are an expert at summarizing resumes/CVs. 

Extract and organize ALL information from the CV into a clean, well-structured outline.

Include:
- Name and contact information
- Education (degrees, institutions, dates)
- Work experience (company, role, dates, key achievements)
- Skills and technologies
- Projects or notable accomplishments
- Any certifications or awards

Format it as a readable outline with clear sections and bullet points.
Be comprehensive - don't leave out any experience or achievement."""

    print("Summarizing CV with OpenAI...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_cv_text}
        ],
        temperature=0.3
    )
    
    summary = response.choices[0].message.content
    
    print(f"✅ Generated CV summary ({len(summary)} characters)")
    
    return summary


def summarize_company_website(website_text: str) -> str:
    """
    Summarize company website text to understand their values, products, and culture.
    
    Args:
        website_text: Text scraped from company website
        
    Returns:
        A clean summary of what the company does and values
    """
    _ensure_openai_key()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = """You are an expert at analyzing and summarizing company websites.

Read through all the content provided and create a comprehensive summary that captures:
- The main purpose and focus of the company
- All key information presented on the website
- Any notable details about what they do, how they operate, and what they value

Be thorough and include everything important. Format as a clear, readable summary."""

    print("Summarizing company website with OpenAI...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": website_text}
        ],
        temperature=0.3
    )
    
    summary = response.choices[0].message.content
    
    print(f"✅ Generated company summary ({len(summary)} characters)")
    
    return summary

