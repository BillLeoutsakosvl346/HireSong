# HireSong Backend

FastAPI backend for generating personalized "hire me" music videos with AI.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# OpenAI API Key (for GPT-4o)
OPENAI_API_KEY=your_openai_api_key_here

# Fal.ai API Key (for Nano Banana images and Kling videos)
FAL_KEY=your_fal_api_key_here

# ElevenLabs API Key (for music generation)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

## Running the API Server

### Development Mode

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

### Production Mode

```bash
python main.py
```

## Testing Individual Services

All test files are in `backend/tests/`:

```bash
# Test CV extraction and summarization
python backend/tests/test_cv_extraction_and_summarisation.py

# Test website scraping
python backend/tests/test_website_scraper.py https://www.anthropic.com

# Test lyrics generation
python backend/tests/test_lyrics_generation.py

# Test scene planning
python backend/tests/test_scene_planning.py

# Test image generation
python backend/tests/test_image_generation.py

# Test video generation
python backend/tests/test_video_generation.py

# Test music generation
python backend/tests/test_music_generation.py
```

## Running the Full Pipeline

### End-to-End Test

```bash
python backend/tests/test_full_pipeline.py
```

This will:
1. Use test files from `backend/tests/test_files/` and `backend/tests/test_images/`
2. Run the complete pipeline asynchronously
3. Save all outputs to `backend/results/test_run/`
4. Verify all generated files

**Expected time:** 2-3 minutes

### Via API

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -F "selfie=@path/to/selfie.jpg" \
  -F "cv=@path/to/cv.pdf" \
  -F "company_url=https://www.anthropic.com"
```

## API Endpoints

### `POST /api/generate`
Generate a complete HireSong video.

**Request:**
- `selfie`: Image file (JPG/PNG)
- `cv`: PDF file
- `company_url`: Company website URL (string)

**Response:**
```json
{
  "status": "success",
  "message": "HireSong video generated successfully!",
  "results": {
    "output_dir": "backend/results/20250101_120000",
    "input_selfie": "...",
    "lyrics": "...",
    "images": ["...", "...", ...],
    "videos": ["...", "...", ...],
    "music": "..."
  }
}
```

### `GET /api/health`
Health check endpoint.

### `GET /api/results/{timestamp}`
Get results manifest for a specific run.

### `GET /api/results/{timestamp}/file/{filename}`
Download a specific file from results.

## Pipeline Architecture

### Async Optimization

The pipeline uses `asyncio` to run operations in parallel:

1. **CV extraction + Website scraping** (parallel)
2. **CV summary + Company summary** (parallel)  
3. **Lyrics generation**
4. **Scene planning**
5. **6 image generations + Music generation** (all parallel)
6. **6 video generations** (parallel)
7. **Video editing** (sequential)

**Time savings:** ~70% faster than sequential processing!

### Output Structure

All outputs are saved to `backend/results/{timestamp}/`:

```
results/20250101_120000/
├── 00_input_selfie.jpg          # Original selfie
├── 00_input_cv.pdf              # Original CV
├── 01_cv_text.txt               # Extracted CV text
├── 01_website_text.txt          # Scraped website text
├── 02_cv_summary.txt            # Summarized CV
├── 02_company_summary.txt       # Summarized company info
├── 03_lyrics.json               # Generated song lyrics
├── 04_scenes.json               # Visual scene plans
├── 05_image_scene_1.jpg         # Generated image 1/6
├── 05_image_scene_2.jpg         # Generated image 2/6
├── ... (4 more images)
├── 06_music.mp3                 # Generated music track
├── 07_video_scene_1.mp4         # Generated video 1/6
├── 07_video_scene_2.mp4         # Generated video 2/6
├── ... (4 more videos)
├── 08_final_video.mp4           # Final edited video (TODO)
└── results_manifest.json        # Manifest with all paths
```

## Architecture

```
backend/
├── api/
│   ├── routes.py               # FastAPI endpoints
│   └── services/
│       ├── orchestrator.py     # Pipeline coordinator (async)
│       ├── text_extraction.py  # PDF text extraction
│       ├── website_scraper.py  # Web scraping
│       ├── summarization.py    # OpenAI summarization
│       ├── lyrics_generation.py # OpenAI lyrics (structured)
│       ├── scene_planning.py   # OpenAI scene planning
│       ├── image_generation.py # Fal.ai Nano Banana
│       ├── video_generation.py # Fal.ai Kling
│       ├── music_generation.py # ElevenLabs
│       └── video_editing.py    # MoviePy (TODO)
├── tests/                      # All test files
├── results/                    # Generated outputs (gitignored)
├── main.py                     # FastAPI app
└── requirements.txt            # Dependencies
```

## Notes

- All generated files are saved for debugging and review
- Results directory is gitignored
- Pipeline is fully async for maximum speed
- Each step can be tested independently
- Structured outputs ensure consistent JSON formats

