"""
Text extraction service for CV PDFs.
Extracts raw text from PDF files.
"""

from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
    """
    print(f"Extracting text from: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    text_parts = []
    
    for page in reader.pages:
        text_parts.append(page.extract_text())
        text_parts.append("\n")
    
    text = "".join(text_parts)
    
    print(f"✅ Extracted {len(text)} characters from {len(reader.pages)} pages")
    
    return text

