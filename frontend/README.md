# HireSong Frontend

React.js frontend for the HireSong AI video pitch generator.

## Features

- 📸 **Webcam Capture**: Take selfies directly in the browser
- 📤 **File Upload**: Upload selfie images and CV PDFs
- 🎥 **Video Generation**: Generate personalized 30-second video pitches
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Clean, professional interface with smooth animations

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Backend Integration

The frontend expects a backend API at `http://localhost:8000` with the following endpoint:

- `POST /api/generate` - Generate video pitch
  - Accepts: multipart/form-data
    - `selfie`: image file
    - `cv`: PDF file
    - `company_url`: string
  - Returns: video/mp4 or JSON with video_url

## Build for Production

```bash
npm run build
```

The production build will be in the `dist` folder.

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Native Web APIs** - Webcam access via getUserMedia
- **CSS3** - Styling with gradients and animations

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── FileUpload.jsx      # File upload component
│   │   ├── WebcamCapture.jsx   # Webcam capture component
│   │   └── VideoPlayer.jsx     # Video playback component
│   ├── App.jsx                 # Main application component
│   ├── App.css                 # Main styles
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html                 # HTML template
├── vite.config.js            # Vite configuration
└── package.json              # Dependencies
```

## Camera Permissions

The webcam feature requires camera permissions. Users will be prompted to allow camera access when clicking "Take Selfie".
