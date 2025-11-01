import os
import json
from PyPDF2 import PdfReader
from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Pydantic typed dictionary declarations.
class CVText(BaseModel):
    text: str = Field(..., description="Text scraped from the CV")

class Contact(BaseModel):
    email: Optional[str] = Field(None, description="Primary email of candidate")
    phone: Optional[str] = Field(None, description="Primary phone number of candidate")

class Experience(BaseModel):
    title: str = Field(..., description="Job title, e.g. 'Senior Software Engineer")
    company: str = Field(..., description="Name of company")
    description: str = Field(..., description="Summary of role/achievements")

class CVData(BaseModel):
    name: str = Field(..., description="Full name of candidate")
    contact: Contact
    experience: List[Experience]

# Load API key from .env file
env_path = os.path.join(os.path.dirname(__file__), "../backend/.env")
load_dotenv(env_path)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_cv_with_openai(raw_cv_text: str) -> CVData:
    """
    Sends raw CV text to GPT-4o and forces structured JSON output.
    
    Args:
        raw_cv_text: The full text extracted from the CV file.
    
    Returns:
        A validated CVData Pydantic object.
    """
    
    system_prompt = (
        """You are an expert resume parsing engine. Extract all relevant details 
        from the user-provided text into the required JSON format.
        Ensure all experience details (title, company, description) are included."""
    )
    
    response = client.chat.completions.create(
        model="gpt-4o", # Modify accordingly
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_cv_text}
        ],
        # Structure output as required
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "CVData",
                "schema": CVData.model_json_schema()
            }
        }
    )
    
    # Get the parsed JSON object from the response
    json_string = response.choices[0].message.content
    
    # Validate the JSON string against the Pydantic model
    return CVData.model_validate_json(json_string)


if __name__ == "__main__":
    # Extract text from pdfs.
    reader = PdfReader("preview_coy/test_files/CoyKZhu_CV.pdf")
    number_of_pages = len(reader.pages)
    textarr = []

    for i in range(number_of_pages):
        page = reader.pages[0]
        pgtext = page.extract_text()
        textarr.append(pgtext)
        textarr.append("\n")

    text = "".join(textarr)

    # Run the parser
    parsed_data = parse_cv_with_openai(text)

    # Convert the Pydantic object to a nicely formatted JSON string for display
    print(json.dumps(parsed_data.model_dump(), indent=4))
