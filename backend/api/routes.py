"""
FastAPI routes for HireSong API.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import tempfile
import shutil

from .services.orchestrator import generate_hiresong_video

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "HireSong API"}


@router.post("/generate")
async def generate_video(
    selfie: UploadFile = File(..., description="Candidate's selfie (JPG/PNG)"),
    cv: UploadFile = File(..., description="Candidate's CV (PDF)"),
    company_url: str = Form(..., description="Target company website URL")
):
    """
    Generate a complete HireSong video.
    
    Accepts:
    - selfie: Image file (JPG/PNG)
    - cv: PDF file
    - company_url: Company website URL (string)
    
    Returns:
    - JSON with paths to all generated files
    """
    
    # Validate file types
    if not selfie.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Selfie must be an image file")
    
    if cv.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="CV must be a PDF file")
    
    # Create temporary files for uploads
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as selfie_temp:
        shutil.copyfileobj(selfie.file, selfie_temp)
        selfie_path = selfie_temp.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as cv_temp:
        shutil.copyfileobj(cv.file, cv_temp)
        cv_path = cv_temp.name
    
    try:
        # Run the pipeline
        results = await generate_hiresong_video(
            selfie_path=selfie_path,
            cv_path=cv_path,
            company_url=company_url
        )
        
        return JSONResponse(content={
            "status": "success",
            "message": "HireSong video generated successfully!",
            "results": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
        
    finally:
        # Clean up temp files
        try:
            os.unlink(selfie_path)
            os.unlink(cv_path)
        except:
            pass


@router.get("/results/{timestamp}")
async def get_results(timestamp: str):
    """
    Get results for a specific timestamp.
    
    Returns the manifest JSON with paths to all files.
    """
    results_dir = os.path.join(
        os.path.dirname(__file__), '..', 'results', timestamp
    )
    manifest_path = os.path.join(results_dir, 'results_manifest.json')
    
    if not os.path.exists(manifest_path):
        raise HTTPException(status_code=404, detail="Results not found")
    
    return FileResponse(manifest_path, media_type='application/json')


@router.get("/results/{timestamp}/file/{filename}")
async def get_result_file(timestamp: str, filename: str):
    """
    Download a specific file from results.
    """
    results_dir = os.path.join(
        os.path.dirname(__file__), '..', 'results', timestamp
    )
    file_path = os.path.join(results_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type based on extension
    ext = os.path.splitext(filename)[1].lower()
    media_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.mp4': 'video/mp4',
        '.mp3': 'audio/mpeg',
        '.pdf': 'application/pdf',
        '.json': 'application/json',
        '.txt': 'text/plain'
    }
    media_type = media_type_map.get(ext, 'application/octet-stream')
    
    return FileResponse(file_path, media_type=media_type)

