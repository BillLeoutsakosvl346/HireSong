# HireSong Frontend - Setup Guide

## Prerequisites

You need to install Node.js and npm first.

### Install Node.js

1. Download Node.js from: https://nodejs.org/
2. Choose the LTS (Long Term Support) version
3. Run the installer and follow the instructions
4. Restart your terminal/PowerShell after installation

### Verify Installation

Open a new PowerShell window and run:
```powershell
node --version
npm --version
```

You should see version numbers for both.

## Setup Instructions

Once Node.js is installed:

1. Navigate to the frontend directory:
```powershell
cd "c:\Users\ZHUCK\Uni\Coding Projects\HireSong\frontend"
```

2. Install dependencies:
```powershell
npm install
```

3. Start the development server:
```powershell
npm run dev
```

4. Open your browser to: http://localhost:3000

## Features Included

✅ **File Upload Component**
   - Upload CV (PDF files)
   - Upload selfie photos
   - Drag and drop support
   - File preview with remove option

✅ **Webcam Capture Component**
   - Take selfies directly in browser
   - Mirror effect for natural selfie experience
   - High-quality capture (1280x720)
   - Camera permission handling

✅ **Video Player Component**
   - Play generated video
   - Download video option
   - Responsive design

✅ **Main Application**
   - Clean, modern UI with gradient background
   - Form validation
   - Loading states
   - Error handling
   - Company URL input
   - Reset functionality

## Usage

1. **Upload or capture your selfie**:
   - Click "Take Selfie" to use your webcam
   - OR click "Upload Photo" to select an image file

2. **Upload your CV**:
   - Click "Upload CV (PDF)" and select your PDF file

3. **Enter company URL**:
   - Type the company website URL (e.g., https://example.com)

4. **Generate video**:
   - Click "Generate Video Pitch 🎬"
   - Wait for the video to be generated
   - Watch and download your personalized pitch!

## Backend Integration

The frontend is configured to communicate with the backend at:
- API endpoint: `http://localhost:8000/api/generate`
- Method: POST
- Content-Type: multipart/form-data

Make sure your backend is running on port 8000 for the frontend to work properly.

## Troubleshooting

### Camera not working
- Make sure you've granted camera permissions in your browser
- Check if another application is using the camera
- Try refreshing the page

### Can't upload files
- Check file types (images: jpg, png, etc.; CV: PDF only)
- Ensure files are not corrupted
- Check file size (large files may take longer)

### Video not generating
- Ensure backend is running on port 8000
- Check browser console for errors (F12)
- Verify all fields are filled correctly

## Production Build

To create a production build:
```powershell
npm run build
```

The optimized files will be in the `dist` folder.

## Technologies Used

- **React 18.2** - Modern React with hooks
- **Vite 5.0** - Fast build tool and dev server
- **Native Web APIs** - Webcam access via getUserMedia API
- **CSS3** - Modern styling with flexbox, gradients, animations
- **Fetch API** - HTTP requests to backend

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── FileUpload.jsx       # File upload with preview
│   │   ├── FileUpload.css
│   │   ├── WebcamCapture.jsx    # Webcam selfie capture
│   │   ├── WebcamCapture.css
│   │   ├── VideoPlayer.jsx      # Video playback & download
│   │   └── VideoPlayer.css
│   ├── App.jsx          # Main application component
│   ├── App.css          # Main application styles
│   ├── main.jsx         # React entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies and scripts
├── .eslintrc.cjs       # ESLint configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file

```

## Development Tips

- The dev server has hot module replacement (HMR) - changes appear instantly
- Use React DevTools browser extension for debugging
- Check browser console for any errors
- The app is fully responsive and works on mobile devices

## Browser Support

Works on all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

Note: Webcam features require HTTPS in production (localhost is fine for development).
