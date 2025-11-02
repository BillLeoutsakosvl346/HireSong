import { useRef, useState, useEffect } from 'react'
import './WebcamCapture.css'

function WebcamCapture({ onCapture }) {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [stream, setStream] = useState(null)
  const [error, setError] = useState(null)
  const [isCameraReady, setIsCameraReady] = useState(false)
  const [showFlash, setShowFlash] = useState(false)

  useEffect(() => {
    startCamera()
    return () => {
      stopCamera()
    }
  }, [])

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

  const handleCapture = () => {
    setShowFlash(true)
    
    // Flash effect then take photo
    setTimeout(() => {
      capturePhoto()
      setShowFlash(false)
    }, 200)
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
        />
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>
      
      <button
        onClick={handleCapture}
        disabled={!isCameraReady}
        className="capture-button"
      >
        {isCameraReady ? '📸 Take Photo' : 'Starting camera...'}
      </button>
    </div>
  )
}

export default WebcamCapture
