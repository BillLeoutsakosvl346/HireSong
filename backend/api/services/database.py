"""
Google Sheets database service for HireSong.
Stores all pipeline runs and their results in a Google Sheet.
"""

import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Sheets configuration
# Get the path relative to this file's location
_current_dir = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(_current_dir, '..', '..', 'hiresong-key.json')
SHEET_ID = "1ZBwSfDbNE9DA5YQ2LVGovLdhtkYzEwwmGiaLvE9E5QA"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Sheet columns (header row)
COLUMNS = [
    "Timestamp",
    "Run ID",
    "Company URL",
    "Genre",
    "Status",
    "CV Summary",
    "Company Summary",
    "Song Title",
    "Song Genre",
    "BPM",
    "Mood",
    "Scene 1 Lyrics",
    "Scene 2 Lyrics",
    "Scene 3 Lyrics",
    "Scene 4 Lyrics",
    "Scene 5 Lyrics",
    "Scene 6 Lyrics",
    "Output Directory",
    "Final Video Path",
    "Music URL",
    "Image URLs",
    "Video URLs",
    "Notes"
]


def _get_sheet():
    """Get authenticated Google Sheets client and worksheet."""
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            print(f"⚠️  Warning: Service account file not found: {SERVICE_ACCOUNT_FILE}")
            print(f"   Please ensure the file exists at: {os.path.abspath(SERVICE_ACCOUNT_FILE)}")
            return None
            
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        return sheet
    except FileNotFoundError as e:
        print(f"⚠️  Warning: Service account file not found: {str(e)}")
        print(f"   Expected location: {os.path.abspath(SERVICE_ACCOUNT_FILE)}")
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not connect to Google Sheets: {str(e)}")
        print(f"   Sheet ID: {SHEET_ID}")
        print(f"   Service account: {SERVICE_ACCOUNT_FILE}")
        return None


def initialize_sheet():
    """
    Initialize the Google Sheet with header row if not already present.
    Call this once to set up the sheet.
    """
    sheet = _get_sheet()
    if not sheet:
        return False
    
    try:
        # Check if header row exists
        first_row = sheet.row_values(1)
        if not first_row or first_row[0] != "Timestamp":
            # Write header row
            sheet.insert_row(COLUMNS, 1)
            print("✅ Initialized Google Sheets database with headers")
        else:
            print("✅ Google Sheets database already initialized")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize sheet: {str(e)}")
        return False


def save_pipeline_start(
    run_id: str,
    company_url: str,
    genre: Optional[str] = None
) -> bool:
    """
    Save initial pipeline run info when starting.
    
    Args:
        run_id: Unique identifier for this run (timestamp)
        company_url: Target company website URL
        genre: Selected music genre (optional)
        
    Returns:
        True if successful, False otherwise
    """
    print(f"📊 Saving to database: Pipeline start (Run ID: {run_id})")
    sheet = _get_sheet()
    if not sheet:
        print("   ⚠️  Skipping - database connection failed")
        return False
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row = [
            timestamp,                          # Timestamp
            run_id,                             # Run ID
            company_url,                        # Company URL
            genre or "AI Selected",             # Genre
            "In Progress",                      # Status
            "",                                 # CV Summary (filled later)
            "",                                 # Company Summary (filled later)
            "",                                 # Song Title (filled later)
            "",                                 # Song Genre (filled later)
            "",                                 # BPM (filled later)
            "",                                 # Mood (filled later)
            "", "", "", "", "", "",             # 6 scene lyrics (filled later)
            "",                                 # Output Directory (filled later)
            "",                                 # Final Video Path (filled later)
            "",                                 # Music URL (filled later)
            "",                                 # Image URLs (filled later)
            "",                                 # Video URLs (filled later)
            "Pipeline started"                  # Notes
        ]
        
        sheet.append_row(row)
        print(f"   ✅ Saved to Google Sheets")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Failed to save: {str(e)}")
        return False


def update_pipeline_progress(
    run_id: str,
    cv_summary: Optional[str] = None,
    company_summary: Optional[str] = None,
    song_data: Optional[Dict[str, Any]] = None,
    output_dir: Optional[str] = None
) -> bool:
    """
    Update pipeline progress with intermediate results.
    
    Args:
        run_id: Unique identifier for this run
        cv_summary: Summarized CV text (optional)
        company_summary: Summarized company info (optional)
        song_data: Song structure data (optional)
        output_dir: Output directory path (optional)
        
    Returns:
        True if successful, False otherwise
    """
    updates = []
    if cv_summary: updates.append("CV summary")
    if company_summary: updates.append("company summary")
    if song_data: updates.append("song data")
    if output_dir: updates.append("output dir")
    
    if updates:
        print(f"📊 Updating database: {', '.join(updates)}")
    
    sheet = _get_sheet()
    if not sheet:
        print("   ⚠️  Skipping - database connection failed")
        return False
    
    try:
        # Find the row with this run_id
        cell = sheet.find(run_id)
        if not cell:
            print(f"⚠️  Warning: Run ID {run_id} not found in sheet")
            return False
        
        row_num = cell.row
        
        # Update CV summary (column 6)
        if cv_summary:
            # Truncate to 500 chars to fit in cell
            sheet.update_cell(row_num, 6, cv_summary[:500])
        
        # Update company summary (column 7)
        if company_summary:
            sheet.update_cell(row_num, 7, company_summary[:500])
        
        # Update song data (columns 8-17)
        if song_data:
            sheet.update_cell(row_num, 8, song_data.get('song_title', '')[:200])
            sheet.update_cell(row_num, 9, song_data.get('genre', ''))
            sheet.update_cell(row_num, 10, str(song_data.get('bpm', '')))
            sheet.update_cell(row_num, 11, song_data.get('mood', '')[:100])
            
            # Update scene lyrics (columns 12-17)
            scenes = song_data.get('scenes', [])
            for i, scene in enumerate(scenes[:6]):
                col_num = 12 + i
                lyrics = scene.get('lyrics', '')[:200]  # Truncate to fit
                sheet.update_cell(row_num, col_num, lyrics)
        
        # Update output directory (column 18)
        if output_dir:
            sheet.update_cell(row_num, 18, output_dir)
        
        print(f"   ✅ Updated in Google Sheets")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Failed to update: {str(e)}")
        return False


def save_pipeline_completion(
    run_id: str,
    final_video_path: str,
    music_url: str,
    image_urls: list,
    video_urls: list,
    status: str = "Completed"
) -> bool:
    """
    Save final pipeline results when completed.
    
    Args:
        run_id: Unique identifier for this run
        final_video_path: Path to final assembled video (local path)
        music_url: URL to generated music file (empty string if not uploaded)
        image_urls: List of Fal.ai image URLs (6 images)
        video_urls: List of Fal.ai video URLs (6 videos)
        status: Status message (default: "Completed")
        
    Returns:
        True if successful, False otherwise
    """
    print(f"📊 Saving to database: Pipeline completion")
    sheet = _get_sheet()
    if not sheet:
        print("   ⚠️  Skipping - database connection failed")
        return False
    
    try:
        # Find the row with this run_id
        cell = sheet.find(run_id)
        if not cell:
            print(f"⚠️  Warning: Run ID {run_id} not found in sheet")
            return False
        
        row_num = cell.row
        
        # Update status (column 5)
        sheet.update_cell(row_num, 5, status)
        
        # Update final video path (column 19)
        sheet.update_cell(row_num, 19, final_video_path)
        
        # Update music URL (column 20)
        sheet.update_cell(row_num, 20, music_url or "Not uploaded")
        
        # Update image URLs (column 21) - join with newlines for readability
        image_urls_str = "\n".join(image_urls) if image_urls else ""
        sheet.update_cell(row_num, 21, image_urls_str)
        
        # Update video URLs (column 22) - join with newlines for readability
        video_urls_str = "\n".join(video_urls) if video_urls else ""
        sheet.update_cell(row_num, 22, video_urls_str)
        
        # Update notes (column 23)
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.update_cell(row_num, 23, f"Completed at {completion_time}")
        
        print(f"   ✅ Saved to Google Sheets")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Failed to save: {str(e)}")
        return False


def save_pipeline_error(
    run_id: str,
    error_message: str
) -> bool:
    """
    Save error information when pipeline fails.
    
    Args:
        run_id: Unique identifier for this run
        error_message: Error message to save
        
    Returns:
        True if successful, False otherwise
    """
    print(f"📊 Saving to database: Pipeline error")
    sheet = _get_sheet()
    if not sheet:
        print("   ⚠️  Skipping - database connection failed")
        return False
    
    try:
        # Find the row with this run_id
        cell = sheet.find(run_id)
        if not cell:
            print(f"⚠️  Warning: Run ID {run_id} not found in sheet")
            return False
        
        row_num = cell.row
        
        # Update status (column 5)
        sheet.update_cell(row_num, 5, "Failed")
        
        # Update notes (column 23)
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_note = f"Failed at {error_time}: {error_message[:300]}"
        sheet.update_cell(row_num, 23, error_note)
        
        print(f"   ✅ Saved to Google Sheets")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Failed to save: {str(e)}")
        return False


def get_all_runs() -> list:
    """
    Get all pipeline runs from the sheet.
    
    Returns:
        List of all runs as dictionaries
    """
    sheet = _get_sheet()
    if not sheet:
        return []
    
    try:
        records = sheet.get_all_records()
        return records
    except Exception as e:
        print(f"⚠️  Warning: Failed to fetch runs from Google Sheets: {str(e)}")
        return []


def get_run_by_id(run_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific pipeline run by its ID.
    
    Args:
        run_id: Unique identifier for the run
        
    Returns:
        Dictionary with run data, or None if not found
    """
    sheet = _get_sheet()
    if not sheet:
        return None
    
    try:
        cell = sheet.find(run_id)
        if not cell:
            return None
        
        row_values = sheet.row_values(cell.row)
        headers = sheet.row_values(1)
        
        # Create dictionary from headers and values
        run_data = {headers[i]: row_values[i] for i in range(len(headers))}
        return run_data
        
    except Exception as e:
        print(f"⚠️  Warning: Failed to fetch run from Google Sheets: {str(e)}")
        return None

