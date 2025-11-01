"""
Website scraper service.
Scrapes text content from company websites.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_website(url: str, max_chars: int = 10000) -> str:
    """
    Scrape text content from a website URL.
    
    Args:
        url: The website URL to scrape
        max_chars: Maximum characters to return (to avoid huge texts)
        
    Returns:
        Scraped text content as a string
    """
    print(f"Scraping website: {url}")
    
    try:
        # Add headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit length
        if len(text) > max_chars:
            text = text[:max_chars]
            print(f"⚠️  Text truncated to {max_chars} characters")
        
        print(f"✅ Scraped {len(text)} characters from {url}")
        
        return text
        
    except requests.exceptions.Timeout:
        raise Exception(f"Timeout while scraping {url}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to scrape {url}: {str(e)}")
    except Exception as e:
        raise Exception(f"Error scraping website: {str(e)}")

