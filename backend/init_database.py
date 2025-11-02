"""
Initialize the Google Sheets database for HireSong.
Run this once to set up the headers in your Google Sheet.
"""

from api.services.database import initialize_sheet

if __name__ == "__main__":
    print("🔧 Initializing Google Sheets database...")
    success = initialize_sheet()
    
    if success:
        print("✅ Database initialized successfully!")
        print("\nYour Google Sheet is now ready to track HireSong pipeline runs.")
        print("\nColumns created:")
        print("  - Timestamp, Run ID, Company URL, Genre, Status")
        print("  - CV Summary, Company Summary")
        print("  - Song Title, Song Genre, BPM, Mood")
        print("  - Scene 1-6 Lyrics")
        print("  - Output Directory, Final Video Path, Music URL")
        print("  - Image URLs (6 Fal.ai image URLs)")
        print("  - Video URLs (6 Fal.ai video URLs)")
        print("  - Notes")
    else:
        print("❌ Failed to initialize database.")
        print("Please check:")
        print("  1. backend/hiresong-key.json exists and has correct permissions")
        print("  2. The service account has edit access to your Google Sheet")
        print("  3. The SHEET_ID in database.py is correct")

