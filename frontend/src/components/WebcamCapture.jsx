import { useRef, useState, useEffect } from 'react'
import './WebcamCapture.css'

function WebcamCapture({ onCapture }) {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [stream, setStream] = useState(null)
  const [error, setError] = useState(null)
  const [isCameraReady, setIsCameraReady] = useState(false)
  const [brightness, setBrightness] = useState(0)
  const [isDragging, setIsDragging] = useState(false)
  const [dragStartTime, setDragStartTime] = useState(null)
  const [showFlash, setShowFlash] = useState(false)
  const lastUpdateRef = useRef(0)

  useEffect(() => {
    startCamera()
    // Reset brightness slowly when not dragging
    if (!isDragging && brightness > 0) {
      const fadeInterval = setInterval(() => {
        setBrightness(prev => Math.max(0, prev - 5))
      }, 50)
      return () => {
        stopCamera()
        clearInterval(fadeInterval)
      }
    }
    return () => {
      stopCamera()
    }
  }, [isDragging, brightness])

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: false,
      })
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      
      setStream(mediaStream)
      setIsCameraReady(true)
      setError(null)
    } catch (err) {
      console.error('Camera error:', err)
      setError('Unable to access camera. Please check permissions.')
    }
  }

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
    }
  }

  const handleBrightnessStart = () => {
    setIsDragging(true)
    setDragStartTime(Date.now())
  }

  const handleBrightnessChange = (e) => {
    if (!isDragging) return
    
    const newBrightness = parseInt(e.target.value)
    
    // Throttle updates to every 100ms for slower, smoother performance
    const now = Date.now()
    if (now - lastUpdateRef.current < 100) {
      return
    }
    lastUpdateRef.current = now
    
    setBrightness(newBrightness)
    
    // If they reach max brightness quickly enough, take the photo!
    if (newBrightness >= 95) {
      const dragDuration = Date.now() - dragStartTime
      if (dragDuration < 1000) { // Must be done within 1 second
        triggerFlashPhoto()
      }
    }
  }

  const handleBrightnessEnd = () => {
    setIsDragging(false)
    setDragStartTime(null)
  }

  const triggerFlashPhoto = () => {
    setIsDragging(false)
    setShowFlash(true)
    setBrightness(100)
    
    // Flash effect then take photo instantly
    setTimeout(() => {
      capturePhoto()
      setShowFlash(false)
    }, 300)
  }

  const capturePhoto = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const context = canvas.getContext('2d')
    context.drawImage(video, 0, 0)
    
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], 'selfie.jpg', { type: 'image/jpeg' })
        onCapture(file)
        stopCamera()
        setBrightness(0)
      }
    }, 'image/jpeg', 0.95)
  }

  if (error) {
    return (
      <div className="webcam-error">
        <p>⚠️ {error}</p>
      </div>
    )
  }

  return (
    <div className="webcam-capture">
      <div className="video-container">
        {showFlash && <div className="flash-overlay" />}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="webcam-video"
          style={{ 
            filter: brightness > 0 ? `brightness(${1 + brightness / 100})` : 'none',
            willChange: isDragging ? 'filter' : 'auto'
          }}
        />
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>
      
      <div className="brightness-control">
        <div className="brightness-label">
          {isCameraReady ? (
            isDragging ? 
              '⚡ Drag fast to the right to take photo!' : 
              '💡 Drag the brightness slider quickly! →'
          ) : (
            'Starting camera...'
          )}
        </div>
        <div className="brightness-slider-container">
          <span className="brightness-icon">🌑</span>
          <input
            type="range"
            min="0"
            max="100"
            value={brightness}
            onChange={handleBrightnessChange}
            onMouseDown={handleBrightnessStart}
            onMouseUp={handleBrightnessEnd}
            onTouchStart={handleBrightnessStart}
            onTouchEnd={handleBrightnessEnd}
            disabled={!isCameraReady}
            className="brightness-slider"
            style={{
              background: `linear-gradient(to right, #333 0%, #ffeb3b ${brightness}%, #ddd ${brightness}%, #ddd 100%)`
            }}
          />
          <span className="brightness-icon">☀️</span>
        </div>
        <div className="brightness-hint">
          {brightness > 0 && brightness < 95 && isDragging && (
            <span className="hint-text">Keep going! {brightness}%</span>
          )}
          {brightness >= 95 && isDragging && (
            <span className="hint-text success">📸 Perfect! Taking photo...</span>
          )}
        </div>
      </div>
    </div>
  )
}

export default WebcamCapture
