# 🎵 HireSong

**Generate personalized AI-powered 30-second music video pitches to land your dream job!**

HireSong is an AI-powered video generator that creates a unique 30-second music video pitch by analyzing your CV, the target company's website, and your selfie. It generates creative lyrics, transforms your photo into funny scenes, animates them, adds music, and assembles everything into a professional (yet ridiculous and memorable) video pitch.

---

## 📖 Table of Contents

- [What is HireSong?](#what-is-hiresong)
- [Architecture Overview](#architecture-overview)
- [How It Works (The Pipeline)](#how-it-works-the-pipeline)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [🚀 Deployment](#-deployment)
- [API Documentation](#api-documentation)
- [Backend Services Explained](#backend-services-explained)
- [Frontend Components Explained](#frontend-components-explained)

---

## 🎬 What is HireSong?

HireSong takes three inputs from you:

1. **Your Selfie** 📸 (captured or uploaded)
2. **Your CV** 📄 (PDF format)
3. **Target Company Website URL** 🏢

And produces:

- ✅ A **30-second music video** with 6 scenes (5 seconds each)
- ✅ **AI-generated song lyrics** that highlight your skills and match the company
- ✅ **Funny, transformed images** of you in ridiculous scenarios
- ✅ **Animated video clips** from those images
- ✅ **Custom music** that matches the lyrics and genre
- ✅ All intermediate outputs saved for review

**Perfect for:** Hackathons, creative job applications, standing out from the crowd, or just having fun!

---

## 🏗️ Architecture Overview

HireSong is built as a **full-stack web application** with three main layers:

### **1. Frontend (React + TypeScript + Vite)**
- Modern, interactive UI for uploading inputs
- Webcam capture functionality
- Real-time video player
- Genre selection dropdown
- Quirky features (button runs away, animated emojis)

### **2. Backend (FastAPI + Python)**
- RESTful API with async processing
- Orchestrated AI pipeline with parallel execution
- Multiple AI service integrations (OpenAI, Fal.ai, ElevenLabs)
- File management and result storage

### **3. AI Services Pipeline**
- **9 sequential steps** with parallel optimizations
- Uses 4 different AI APIs
- Saves all intermediate results for debugging

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
│  [Upload UI] → [Genre Selector] → [Loading] → [Video Player]   │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP POST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│                                                                 │
│  [Routes] → [Orchestrator] → [9-Step AI Pipeline]              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              AI SERVICES (async/parallel)                │  │
│  │                                                          │  │
│  │  OpenAI GPT-5    Fal.ai         ElevenLabs   MoviePy   │  │
│  │  (Lyrics/AI)  (Images/Videos)    (Music)    (Assembly)  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [Results Storage] → saves all outputs to timestamped folders  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ How It Works (The Pipeline)

HireSong runs a **9-step orchestrated pipeline** when you click "Generate":

### **Step 1 & 2: Data Extraction (Parallel)**
- **Extract CV text** from PDF using PyPDF2
- **Scrape company website** using BeautifulSoup
- ⏱️ Both run in parallel to save time

### **Step 3: Summarization (Parallel)**
- **Summarize CV** → Extracts key skills, experience, education
- **Summarize Company** → Identifies mission, values, technologies
- Uses OpenAI GPT-4o for intelligent summarization
- ⏱️ Both summaries generated in parallel

### **Step 4: Lyrics Generation**
- Uses **OpenAI GPT-5** with structured outputs (Pydantic models)
- Takes CV summary + company summary + optional genre
- Generates 6 scenes with lyrics, each timed for 5 seconds
- Adjusts word count based on genre (Rap: 15-20 words, Pop: 8-12 words)
- Output: `03_lyrics.json`

### **Step 5: Scene Planning**
- Uses **OpenAI GPT-5** to create visual plans for each scene
- For each scene, generates:
  - Scene description (what happens)
  - Image prompt (for Nano Banana to transform selfie)
  - Video prompt (for Kling to animate the image)
- Ensures scenes are funny, coherent, and preserve facial features
- Output: `04_scenes.json`

### **Step 6: Image Generation (Parallel)**
- Uses **Fal.ai Nano Banana** to transform selfie into 6 funny images
- Each image corresponds to one scene
- Selfie + image prompt → transformed image
- ⏱️ All 6 images generated in parallel
- Output: `05_image_scene_1.jpg` through `05_image_scene_6.jpg`

### **Step 7: Video Generation (Parallel)**
- Uses **Fal.ai Kling 2.5 Pro** for image-to-video conversion
- Each image + video prompt → 5-second animated video
- ⏱️ All 6 videos generated in parallel
- Output: `07_video_scene_1.mp4` through `07_video_scene_6.mp4`

### **Step 8: Music Generation**
- Uses **ElevenLabs Music API** to generate a 30-second song
- Takes: genre, BPM, mood, instrumentation, and all lyrics
- Creates music that matches the song structure
- Output: `06_music.mp3`

### **Step 9: Video Assembly**
- Uses **MoviePy v2** to combine everything
- Concatenates 6 videos (5 seconds each = 30 seconds)
- Adds the 30-second music track
- (Optional) Overlays lyrics at the bottom
- Output: `08_final_video.mp4` 🎉

**Total Time:** ~3-5 minutes (depending on AI API response times)

---

## 🛠️ Tech Stack

### **Frontend**
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **CSS3** - Custom styling with gradients and animations
- **Webcam API** - For selfie capture

### **Backend**
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Python 3.12** - Programming language
- **Asyncio** - Asynchronous task execution

### **AI Services**
- **OpenAI GPT-5** - Lyrics generation, scene planning, summarization
- **Fal.ai Nano Banana** - Image transformation (selfie → funny scenes)
- **Fal.ai Kling 2.5 Pro** - Image-to-video animation
- **ElevenLabs Music API** - Music generation

### **Libraries & Tools**
- **Pydantic** - Data validation and structured outputs
- **PyPDF2** - PDF text extraction
- **BeautifulSoup4** - Web scraping
- **MoviePy v2** - Video editing and assembly
- **python-dotenv** - Environment variable management
- **Requests** - HTTP client for API calls

---

## 📁 Project Structure

```
HireSong/
├── backend/                          # Python FastAPI backend
│   ├── main.py                       # FastAPI app entry point
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # API keys (not in repo)
│   ├── api/
│   │   ├── routes.py                 # API endpoints (/api/generate, /api/health)
│   │   └── services/                 # Core AI services
│   │       ├── orchestrator.py       # Pipeline coordinator (9 steps)
│   │       ├── text_extraction.py    # Extract text from PDF
│   │       ├── website_scraper.py    # Scrape company websites
│   │       ├── summarization.py      # AI summarization (CV & company)
│   │       ├── lyrics_generation.py  # Generate song lyrics (GPT-5)
│   │       ├── scene_planning.py     # Plan visual scenes (GPT-5)
│   │       ├── image_generation.py   # Transform selfie (Nano Banana)
│   │       ├── video_generation.py   # Animate images (Kling)
│   │       ├── music_generation.py   # Generate music (ElevenLabs)
│   │       └── assembling_video.py   # Combine everything (MoviePy)
│   ├── tests/                        # Unit tests for each service
│   │   ├── test_full_pipeline.py     # End-to-end pipeline test
│   │   ├── test_lyrics_generation.py # Test lyrics with/without genre
│   │   ├── test_image_generation.py  # Test image transformation
│   │   ├── test_video_generation.py  # Test video animation
│   │   ├── test_music_generation.py  # Test music creation
│   │   └── test_files/               # Test data (CV, selfie, etc.)
│   └── results/                      # Generated outputs (gitignored)
│       └── {timestamp}/              # Each run gets a timestamped folder
│           ├── 00_input_selfie.jpg
│           ├── 00_input_cv.pdf
│           ├── 01_cv_text.txt
│           ├── 01_website_text.txt
│           ├── 02_cv_summary.txt
│           ├── 02_company_summary.txt
│           ├── 03_lyrics.json
│           ├── 04_scenes.json
│           ├── 05_image_scene_*.jpg  # 6 images
│           ├── 06_music.mp3
│           ├── 07_video_scene_*.mp4  # 6 videos
│           ├── 08_final_video.mp4    # 🎉 FINAL OUTPUT
│           └── results_manifest.json
│
├── frontend/                         # React TypeScript frontend
│   ├── index.html                    # HTML entry point
│   ├── package.json                  # Node dependencies
│   ├── vite.config.js                # Vite configuration
│   └── src/
│       ├── main.jsx                  # React app entry
│       ├── App.jsx                   # Main app component
│       ├── App.css                   # App styling
│       ├── index.css                 # Global styles
│       └── components/
│           ├── FileUpload.jsx        # File upload component
│           ├── WebcamCapture.jsx     # Webcam selfie capture
│           └── VideoPlayer.jsx       # Final video display
│
└── README.md                         # This file!
```

---

## 🚀 Setup & Installation

### **Prerequisites**
- **Python 3.12+**
- **Node.js 18+** and npm
- **API Keys** for:
  - OpenAI (GPT-5)
  - Fal.ai (for Nano Banana and Kling)
  - ElevenLabs (for music)

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd HireSong
```

### **2. Backend Setup**

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
FAL_KEY=your_fal_api_key_here
ELEVENLABS_KEY=your_elevenlabs_api_key_here
EOF
```

### **3. Frontend Setup**

```bash
# Navigate to frontend
cd ../frontend

# Install Node dependencies
npm install
```

---

## 🏃 Running the Application

### **Start Backend (Terminal 1)**

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend runs on: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

### **Start Frontend (Terminal 2)**

```bash
cd frontend
npm run dev
```

Frontend runs on: **http://localhost:5173**

### **Open in Browser**

Visit **http://localhost:5173** and:
1. Upload or capture your selfie
2. Upload your CV (PDF)
3. Enter company website URL
4. (Optional) Select music genre
5. Click "Generate Video Pitch" 🎬
6. Wait ~3-5 minutes ☕
7. Watch your personalized music video! 🎉

---

## 🚀 Deployment

Ready to deploy your HireSong app online? **See the complete deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

### Quick Overview

**Recommended Stack:**
- **Backend:** Railway (handles long-running processes, no timeouts)
- **Frontend:** Vercel (fast, free, global CDN)

**Why not Vercel for backend?**
- Vercel has 10-60 second timeouts
- Your pipeline takes 2-3 minutes
- Railway has no timeout limits and supports persistent processes

**Deployment Time:**
- Backend on Railway: ~5 minutes
- Frontend on Vercel: ~3 minutes
- Total: **~8 minutes** ⚡

**What you need:**
- Railway account (free tier: $5 credit/month)
- Vercel account (free tier: unlimited for frontend)
- Your API keys (OpenAI, Fal, ElevenLabs)
- Google Sheets credentials (`hiresong-key.json`)

**Quick Start:**
```bash
# Deploy backend to Railway
cd backend
railway init
railway up

# Deploy frontend to Vercel
cd frontend
vercel
```

**Full instructions:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📡 API Documentation

### **POST /api/generate**

Generate a complete HireSong video.

**Request:**
- `Content-Type`: `multipart/form-data`
- `selfie` (file): Image file (JPG/PNG)
- `cv` (file): PDF file
- `company_url` (string): Company website URL
- `genre` (string, optional): Music genre (e.g., "Pop", "Rap", "Surprise Me")

**Response:**
- Returns MP4 video file directly
- `Content-Type`: `video/mp4`
- File name: `hiresong_pitch.mp4`

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/generate \
  -F "selfie=@selfie.jpg" \
  -F "cv=@resume.pdf" \
  -F "company_url=https://anthropic.com" \
  -F "genre=Pop" \
  --output my_pitch.mp4
```

### **GET /api/health**

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "HireSong API"
}
```

### **GET /api/results/{timestamp}**

Get results manifest for a specific run.

**Response:**
```json
{
  "output_dir": "backend/results/20251101_192017",
  "timestamp": "2025-11-01T19:20:17",
  "input_selfie": "00_input_selfie.jpg",
  "input_cv": "00_input_cv.pdf",
  "final_video": "08_final_video.mp4",
  ...
}
```

### **GET /api/results/{timestamp}/file/{filename}**

Download a specific result file.

**Example:**
```
GET /api/results/20251101_192017/file/08_final_video.mp4
```

---

## 🧩 Backend Services Explained

### **1. `orchestrator.py` - Pipeline Coordinator**

**Purpose:** Orchestrates the entire 9-step pipeline with async optimization.

**Key Functions:**
- `generate_hiresong_video()` - Main entry point
- Uses `asyncio.gather()` to run independent tasks in parallel
- Saves all intermediate outputs to timestamped folders
- Returns paths to all generated files

**Optimizations:**
- Steps 1-2 run in parallel (CV extraction + website scraping)
- Step 3 runs in parallel (CV summary + company summary)
- Step 6 runs in parallel (6 images generated simultaneously)
- Step 7 runs in parallel (6 videos generated simultaneously)

---

### **2. `text_extraction.py` - PDF Parser**

**Purpose:** Extract raw text from PDF files.

**Key Functions:**
- `extract_text_from_pdf(pdf_path)` - Extracts all text from CV

**Technology:** PyPDF2

---

### **3. `website_scraper.py` - Web Scraper**

**Purpose:** Scrape and extract clean text from company websites.

**Key Functions:**
- `scrape_website(url)` - Fetches and parses HTML, returns clean text

**Technology:** Requests + BeautifulSoup4

**Cleaning:**
- Removes script/style tags
- Extracts visible text only
- Handles errors gracefully

---

### **4. `summarization.py` - AI Summarization**

**Purpose:** Use OpenAI to create concise summaries of CV and company info.

**Key Functions:**
- `summarize_cv(cv_text)` - Summarizes CV highlighting skills, experience
- `summarize_company_website(website_text)` - Summarizes company mission, values, tech

**Technology:** OpenAI GPT-4o

**Output:** Clean, structured text summaries

---

### **5. `lyrics_generation.py` - Song Lyrics Creator**

**Purpose:** Generate creative, funny song lyrics that match CV and company.

**Key Functions:**
- `generate_song_lyrics(cv_summary, company_summary, preferred_genre=None)` - Creates song structure

**Technology:** OpenAI GPT-5 with structured outputs (Pydantic)

**Features:**
- 6 scenes, 5 seconds each
- Genre-aware word counts (Rap: 15-20, Pop: 8-12, Ballad: 5-8)
- User can select genre or let AI choose
- Ensures funny, memorable lyrics

**Output:** JSON with title, genre, BPM, mood, instrumentation, and 6 scenes with lyrics

---

### **6. `scene_planning.py` - Visual Scene Planner**

**Purpose:** Plan detailed visual scenes for each 5-second segment.

**Key Functions:**
- `generate_scene_plan(cv_summary, company_summary, song_structure)` - Creates visual plans

**Technology:** OpenAI GPT-5 with structured outputs

**For Each Scene:**
- **Description:** What the person is doing
- **Image Prompt:** For Nano Banana to transform selfie
- **Video Prompt:** For Kling to animate the image

**Important:**
- Preserves facial features
- Changes everything else (background, clothes, props)
- No specific names or company names in prompts
- Funny and ridiculous scenarios

---

### **7. `image_generation.py` - Selfie Transformer**

**Purpose:** Transform selfie into 6 different funny scenes.

**Key Functions:**
- `generate_image_from_prompt(selfie_path, prompt)` - Transforms selfie using image prompt

**Technology:** Fal.ai Nano Banana

**Process:**
- Uploads selfie to Fal storage
- Sends prompt + selfie reference
- Returns transformed image URL
- Downloads and saves image

---

### **8. `video_generation.py` - Image Animator**

**Purpose:** Animate static images into 5-second videos.

**Key Functions:**
- `generate_video_from_url(image_url, prompt, duration=5)` - Animates image

**Technology:** Fal.ai Kling 2.5 Pro (image-to-video)

**Settings:**
- Duration: 5 seconds per scene
- Aspect ratio: 16:9
- Returns video URL
- Downloads and saves video

---

### **9. `music_generation.py` - Music Composer**

**Purpose:** Generate 30-second music that matches the song structure.

**Key Functions:**
- `generate_music(song_data)` - Creates music from song structure

**Technology:** ElevenLabs Music API

**Input:** Genre, BPM, mood, instrumentation, all 6 scene lyrics

**Output:** 30-second MP3 audio file

---

### **10. `assembling_video.py` - Video Editor**

**Purpose:** Combine all videos with music into final 30-second video.

**Key Functions:**
- `assemble_final_video(video_1...video_6, music_path, output_path, lyrics=None)` - Creates final video
- `assemble_from_list(video_paths, music_path, output_path, lyrics=None)` - Convenience wrapper

**Technology:** MoviePy v2

**Process:**
- Loads 6 videos, forces each to exactly 5 seconds
- Concatenates them (6 × 5s = 30s)
- Loads music, forces to exactly 30 seconds (loops if shorter, trims if longer)
- Attaches audio
- (Optional) Adds lyrics overlay at bottom
- Exports as MP4

---

## 🎨 Frontend Components Explained

### **1. `App.jsx` - Main Application**

**Purpose:** Main app logic and state management.

**State:**
- `selfieFile`, `cvFile`, `companyUrl`, `genre` - User inputs
- `videoUrl` - Generated video URL
- `isGenerating` - Loading state
- `error` - Error messages
- `showWebcam` - Webcam visibility
- `buttonPosition`, `encouragementCount` - Quirky button behavior

**Features:**
- Form validation
- Uploads files to backend API
- Displays loading state
- Shows final video
- **Quirky feature:** Generate button runs away when you hover (gets tired after 7 attempts)

---

### **2. `FileUpload.jsx` - File Upload Component**

**Purpose:** Reusable file upload component with drag-and-drop.

**Props:**
- `label` - Button label
- `accept` - File types to accept
- `onFileSelect` - Callback when file is selected
- `file` - Currently selected file
- `fileType` - "image" or "pdf" for preview

**Features:**
- Visual file preview
- Shows file name and size
- Remove button

---

### **3. `WebcamCapture.jsx` - Webcam Selfie Capture**

**Purpose:** Capture selfie directly from webcam.

**Features:**
- Uses browser's `getUserMedia` API
- Live video preview
- Capture button
- Retake functionality
- Converts to Blob for upload

---

### **4. `VideoPlayer.jsx` - Video Display**

**Purpose:** Display the final generated video.

**Props:**
- `videoUrl` - URL to the video

**Features:**
- HTML5 video player
- Controls (play, pause, seek, volume)
- Download button
- Responsive sizing

---

## 🧪 Testing

Run individual service tests:

```bash
# Test lyrics generation
python backend/tests/test_lyrics_generation.py

# Test image generation
python backend/tests/test_image_generation.py

# Test video generation
python backend/tests/test_video_generation.py

# Test music generation
python backend/tests/test_music_generation.py

# Test full pipeline (end-to-end)
python backend/tests/test_full_pipeline.py
```

---

## 🎯 Key Features

✨ **Async Processing:** Parallel execution of independent tasks reduces total time by ~50%

✨ **Structured Outputs:** Uses Pydantic models to ensure AI responses are properly formatted

✨ **Genre Selection:** User can choose music genre or let AI decide

✨ **Complete Transparency:** All intermediate files saved for debugging

✨ **Quirky UI:** Fun animations and Easter eggs (button that runs away)

✨ **WebRTC:** Webcam integration for selfie capture

✨ **Responsive:** Works on desktop and mobile

---

## 📝 Environment Variables

Create a `backend/.env` file:

```env
# OpenAI (for GPT-5 lyrics and scene planning)
OPENAI_API_KEY=sk-...

# Fal.ai (for image and video generation)
FAL_KEY=...

# ElevenLabs (for music generation)
ELEVENLABS_KEY=...
```

---

## 🐛 Troubleshooting

**"Module not found" errors:**
```bash
pip install -r backend/requirements.txt
```

**"API key not found" errors:**
- Check `backend/.env` file exists
- Verify API keys are correct
- Ensure no extra spaces or quotes

**"Port already in use":**
```bash
# Backend (change port)
uvicorn main:app --reload --port 8001

# Frontend (change port)
npm run dev -- --port 3000
```

**Video generation fails:**
- Check Fal.ai API key
- Ensure input image is valid
- Check Fal.ai API status

**MoviePy errors:**
- Ensure moviepy v2 is installed: `pip install moviepy==1.0.3`
- Check ffmpeg is available in PATH

---

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [OpenAI API](https://platform.openai.com/docs)
- [Fal.ai Docs](https://fal.ai/docs)
- [ElevenLabs API](https://elevenlabs.io/docs)
- [MoviePy Docs](https://zulko.github.io/moviepy/)

---

## 📄 License

This is a hackathon project. Feel free to use, modify, and share!

---

## 🙏 Acknowledgments

Built with ❤️ using amazing AI tools:
- OpenAI GPT-5
- Fal.ai (Nano Banana & Kling)
- ElevenLabs Music

---

## 🚀 Future Improvements

- [ ] Add lyrics overlay (timing issues to fix)
- [ ] Support more video aspect ratios (9:16 for TikTok)
- [ ] Add voice narration option
- [ ] Database for storing user videos
- [ ] Social media sharing buttons
- [ ] More customization options (colors, fonts, effects)
- [ ] Real-time progress updates with WebSockets
- [ ] Queue system for multiple concurrent users

---

**Made with 🎵 and a lot of ☕ for hackathons!**

