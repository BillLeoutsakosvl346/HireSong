# HireSong - Project Plan

## Overview

HireSong is a hackathon project that generates personalized 30-second "hire me" music video pitches. Users upload a selfie, CV, and company website URL, and the system creates a TikTok-length video combining AI-generated visuals and music.

**Tech Stack:**
- Backend: Python + FastAPI
- Frontend: TypeScript + React + Vite
- AI Services: OpenAI (LLM), Fal.ai (Nano Banana for images, Kling 2.5 Pro for video), Suno v5 (music)
- Storage: In-memory (hackathon simplicity)

---

## The Pipeline (8 Steps)

1. **Text Extraction** - Extract text from CV PDF and scrape company website
2. **Summarization** - Generate structured CV summary and company summary
3. **Scene Planning** - Create 6-scene structure with visual prompts and timing (5s each)
4. **Visual Generation** - Generate images and convert to video clips using Fal.ai
5. **Lyrics Generation** - Write 25-30s lyrics matching scene beats
6. **Music Generation** - Create audio track from lyrics using Suno
7. **Video Editing** - Concatenate 6 clips and add audio track
8. **Delivery** - Return final MP4 to frontend

---

## Backend Structure

### Root (`/backend`)

```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── api/                 # API routes
├── services/            # Business logic (8 service modules)
├── models/              # Pydantic schemas
├── utils/               # Helper functions
└── storage/             # In-memory storage
```

### `/api` - API Routes
- `routes.py` - Single `/generate` POST endpoint
  - Input: selfie (image), CV (PDF), company_url (string)
  - Output: video file (MP4) or video_id

### `/services` - Business Logic (One file per pipeline step)
- `orchestrator.py` - Main pipeline coordinator
- `text_extraction.py` - PyPDF2 + BeautifulSoup scraping
- `summarization.py` - OpenAI GPT summaries
- `scene_planning.py` - OpenAI 6-scene structure generation
- `visual_generation.py` - Fal.ai image + video generation
- `lyrics_generation.py` - OpenAI lyrics writing
- `music_generation.py` - Suno v5 audio generation
- `video_editing.py` - MoviePy video assembly

### `/models` - Data Models
- `schemas.py` - Pydantic models:
  - `GenerateRequest` - Upload form data
  - `CVSummary` - Structured CV summary
  - `CompanySummary` - Structured company summary
  - `ScenePlan` - 6 scenes with prompts/timing
  - `GenerateResponse` - Final video data

### `/utils` - Utilities
- `api_clients.py` - OpenAI, Fal, Suno client wrappers with error handling
- `file_helpers.py` - File operations, unique ID generation

### `/storage` - Storage
- `memory_store.py` - Dict-based in-memory storage for job status and video bytes

### Dependencies (`requirements.txt`)
```
fastapi
uvicorn[standard]
openai
fal-client
moviepy
PyPDF2
beautifulsoup4
requests
python-multipart
python-dotenv
```

---

## Frontend Structure

### Root (`/frontend`)

```
frontend/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── index.html
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── components/
    │   ├── UploadForm.tsx
    │   ├── LoadingScreen.tsx
    │   └── VideoPlayer.tsx
    ├── services/
    │   └── api.ts
    ├── types/
    │   └── index.ts
    └── styles/
        └── index.css
```

### `/src` - Source Files
- `main.tsx` - React DOM render entry point
- `App.tsx` - Main app component with state management (upload → loading → result)

### `/src/components` - UI Components
- `UploadForm.tsx` - File dropzone (selfie + CV) + text input (company URL) + submit
- `LoadingScreen.tsx` - Progress indicator with step labels
- `VideoPlayer.tsx` - HTML5 video player with download button

### `/src/services` - API Layer
- `api.ts` - Axios client with `/api/generate` POST method

### `/src/types` - TypeScript Types
- `index.ts` - TypeScript interfaces matching backend Pydantic schemas

### `/src/styles` - Styling
- `index.css` - Modern minimal CSS (can add Tailwind later)

### Dependencies (`package.json`)
```json
{
  "dependencies": {
    "react",
    "react-dom",
    "axios",
    "react-dropzone"
  },
  "devDependencies": {
    "@types/react",
    "@types/react-dom",
    "@vitejs/plugin-react",
    "typescript",
    "vite"
  }
}
```

### Vite Config
- Proxy `/api/*` requests to backend (`http://localhost:8000`)

---

## Key Design Decisions

### 1. Synchronous Pipeline
- Single `/api/generate` endpoint handles full pipeline
- Frontend shows loading screen during processing (25-45s)
- Simpler than async/polling for hackathon

### 2. In-Memory Storage
- Videos stored in Python dict with unique job IDs
- No database, no persistence across restarts
- Fast and simple for demo purposes

### 3. Error Handling
- Try-catch blocks in each service module
- Descriptive error messages returned to frontend
- Basic validation on uploads (file types, sizes)

### 4. CORS Configuration
- Backend allows localhost:5173 (Vite default) for development
- Simple configuration for hackathon environment

### 5. File Upload
- Multipart form data for selfie + CV
- Company URL as form field
- Validate image formats (JPEG, PNG) and PDF

---

## Development Workflow

### Backend Setup
1. Create virtual environment
2. Install dependencies from requirements.txt
3. Copy .env.example to .env and add API keys
4. Run: `uvicorn backend.main:app --reload`
5. API available at http://localhost:8000

### Frontend Setup
1. Install dependencies: `npm install`
2. Run dev server: `npm run dev`
3. Frontend available at http://localhost:5173

### Testing Flow
1. Upload selfie (JPEG/PNG)
2. Upload CV (PDF)
3. Enter company URL
4. Submit and wait 25-45 seconds
5. Watch/download generated video

---

## API Contract

### POST `/api/generate`

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `selfie`: File (image/jpeg or image/png)
  - `cv`: File (application/pdf)
  - `company_url`: string (URL)

**Response (Success):**
```json
{
  "success": true,
  "video_url": "/api/video/{job_id}",
  "job_id": "uuid-string",
  "duration": 30
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message here",
  "step": "visual_generation"
}
```

### GET `/api/video/{job_id}`

**Response:**
- Content-Type: `video/mp4`
- Binary video file

---

## Implementation Order

### Phase 1: Backend Foundation
1. Create folder structure with __init__.py files
2. Set up main.py with FastAPI app and CORS
3. Define Pydantic schemas in models/schemas.py
4. Create .env.example template

### Phase 2: Service Layer
5. Implement utils (api_clients.py, file_helpers.py)
6. Implement text_extraction.py (PDF + web scraping)
7. Implement summarization.py (OpenAI)
8. Implement scene_planning.py (OpenAI)
9. Implement visual_generation.py (Fal.ai)
10. Implement lyrics_generation.py (OpenAI)
11. Implement music_generation.py (Suno)
12. Implement video_editing.py (MoviePy)

### Phase 3: API Integration
13. Implement orchestrator.py (pipeline coordinator)
14. Implement api/routes.py (FastAPI endpoints)
15. Test backend pipeline end-to-end

### Phase 4: Frontend
16. Initialize Vite + React + TypeScript project
17. Set up vite.config.ts with proxy
18. Create TypeScript types
19. Implement api.ts service
20. Build UploadForm component
21. Build LoadingScreen component
22. Build VideoPlayer component
23. Wire up App.tsx with state management
24. Add styling

### Phase 5: Integration & Testing
25. Test full flow locally
26. Debug and refine
27. Prepare demo

---

## Future Enhancements (Post-Hackathon)

- Persistent storage (database + S3)
- Async processing with job queue
- WebSocket for real-time progress updates
- User accounts and video gallery
- Multiple video styles/templates
- Advanced scene customization
- Social sharing features
- Analytics and A/B testing

---

## Notes

- Keep it simple - this is a hackathon project
- Focus on the core pipeline working end-to-end
- Don't over-engineer - in-memory storage is fine
- Prioritize demo-ability over production features
- Make the UI clean and modern (first impressions matter)
- Have fun with the AI prompts - make videos engaging!

