import { useState, useEffect } from 'react'
import FileUpload from './components/FileUpload'
import WebcamCapture from './components/WebcamCapture'
import VideoPlayer from './components/VideoPlayer'
import './App.css'

function App() {
  // API URL from environment variable (for deployment) or default to local
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const [selfieFile, setSelfieFile] = useState(null)
  const [cvFile, setCvFile] = useState(null)
  const [companyUrl, setCompanyUrl] = useState('')
  const [genre, setGenre] = useState('Surprise Me')
  const [isGenerating, setIsGenerating] = useState(false)
  const [videoUrl, setVideoUrl] = useState(null)
  const [error, setError] = useState(null)
  const [showWebcam, setShowWebcam] = useState(false)
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 })
  const [encouragementCount, setEncouragementCount] = useState(0)
  const [headerEmoji, setHeaderEmoji] = useState('🎵')

  // Change header emoji randomly
  useEffect(() => {
    const emojis = ['🎵', '🎶', '🎤', '🎸', '🎹', '🎺', '🎻', '🥁', '🎧', '💼', '🎬', '✨']
    const interval = setInterval(() => {
      setHeaderEmoji(emojis[Math.floor(Math.random() * emojis.length)])
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  const handleSelfieCapture = (imageBlob) => {
    setSelfieFile(imageBlob)
    setShowWebcam(false)
  }

  const handleSelfieUpload = (file) => {
    setSelfieFile(file)
  }

  const handleCvUpload = (file) => {
    setCvFile(file)
  }

  const handleGenerateMouseEnter = () => {
    // Button runs away when you hover over it (if all fields are filled)
    if (selfieFile && cvFile && companyUrl && !isGenerating) {
      // After 7+ attempts (when "Fine, you can click me now" appears), move much less
      const isTired = encouragementCount >= 7
      
      const maxMoveX = isTired ? 30 : 200
      const maxMoveY = isTired ? 20 : 150
      
      const randomX = (Math.random() - 0.5) * maxMoveX
      const randomY = (Math.random() - 0.5) * maxMoveY
      setButtonPosition({ x: randomX, y: randomY })
      setEncouragementCount(prev => prev + 1)
    }
  }

  const handleGenerate = async () => {
    // Validation
    if (!selfieFile) {
      setError('Please upload or capture a selfie')
      return
    }
    if (!cvFile) {
      setError('Please upload your CV (PDF)')
      return
    }
    if (!companyUrl || !companyUrl.trim()) {
      setError('Please enter the company website URL')
      return
    }

    setError(null)
    setIsGenerating(true)
    setVideoUrl(null)
    setButtonPosition({ x: 0, y: 0 }) // Reset button position

    try {
      const formData = new FormData()
      formData.append('selfie', selfieFile)
      formData.append('cv', cvFile)
      formData.append('company_url', companyUrl)
      formData.append('genre', genre)

      const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Server error: ${response.status}`)
      }

      // Check if response is a video file
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('video')) {
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        setVideoUrl(url)
      } else {
        const data = await response.json()
        if (data.video_url) {
          setVideoUrl(data.video_url)
        } else {
          throw new Error('No video URL in response')
        }
      }
    } catch (err) {
      console.error('Generation error:', err)
      setError(err.message || 'Failed to generate video. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleReset = () => {
    setSelfieFile(null)
    setCvFile(null)
    setCompanyUrl('')
    setGenre('Surprise Me')
    setVideoUrl(null)
    setError(null)
    setShowWebcam(false)
    setButtonPosition({ x: 0, y: 0 })
    setEncouragementCount(0)
  }

  // Encouragement messages when button runs away
  const getEncouragementMessage = () => {
    const messages = [
      "Come on, you can do it! 🏃",
      "Almost there! Keep trying! 💪",
      "The button believes in you! ✨",
      "Third time's the charm! 🍀",
      "You're getting warmer! 🔥",
      "Don't give up now! 🎯",
      "Catch me if you can! 😄",
      "Fine, you can click me now... 😌"
    ]
    const index = Math.min(encouragementCount - 1, messages.length - 1)
    return encouragementCount > 0 ? messages[index] : null
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>{headerEmoji} HireSong</h1>
          <p>Generate your personalized AI-powered video pitch in 30 seconds</p>
        </header>

        {!videoUrl ? (
          <div className="upload-section">
            {/* Selfie Section */}
            <div className="input-group">
              <h2>📸 Your Selfie</h2>
              <div className="button-group">
                <button
                  className="btn btn-secondary"
                  onClick={() => setShowWebcam(!showWebcam)}
                >
                  {showWebcam ? 'Cancel Camera' : 'Take Selfie'}
                </button>
                <span className="or-text">or</span>
                <FileUpload
                  label="Upload Photo"
                  accept="image/*"
                  onFileSelect={handleSelfieUpload}
                  file={selfieFile}
                  fileType="image"
                />
              </div>
              {showWebcam && (
                <WebcamCapture onCapture={handleSelfieCapture} />
              )}
              {selfieFile && !showWebcam && (
                <div className="preview">
                  <img
                    src={URL.createObjectURL(selfieFile)}
                    alt="Selfie preview"
                    className="preview-image"
                  />
                  <button
                    className="btn-remove"
                    onClick={() => setSelfieFile(null)}
                  >
                    ✕
                  </button>
                </div>
              )}
            </div>

            {/* CV Upload Section */}
            <div className="input-group">
              <h2>📄 Your CV</h2>
              <FileUpload
                label="Upload CV (PDF)"
                accept=".pdf,application/pdf"
                onFileSelect={handleCvUpload}
                file={cvFile}
                fileType="pdf"
              />
            </div>

            {/* Company URL Section */}
            <div className="input-group">
              <h2>🏢 Company Website</h2>
              <input
                type="url"
                placeholder="https://example.com"
                value={companyUrl}
                onChange={(e) => setCompanyUrl(e.target.value)}
                className="url-input"
              />
            </div>

            {/* Genre Selection */}
            <div className="input-group">
              <h2>🎸 Music Genre</h2>
              <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                className="genre-select"
              >
                <option value="Surprise Me">🎲 Surprise Me</option>
                <option value="Pop">🎤 Pop</option>
                <option value="Rock">🎸 Rock</option>
                <option value="Rap">🎤 Rap / Hip-Hop</option>
                <option value="Electronic">🎧 Electronic / Dance</option>
                <option value="Country">🤠 Country</option>
                <option value="Jazz">🎷 Jazz</option>
                <option value="R&B">💿 R&B</option>
                <option value="Metal">🤘 Metal</option>
                <option value="Indie">🎹 Indie</option>
                <option value="Ballad">🎻 Ballad</option>
              </select>
              <p className="hint-text">Choose a music genre for your pitch song, or let AI surprise you!</p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}

            {/* Encouragement Message */}
            {getEncouragementMessage() && (
              <div className="encouragement-message">
                {getEncouragementMessage()}
              </div>
            )}

            {/* Generate Button - with runaway behavior */}
            <div className="button-wrapper">
              <button
                className="btn btn-primary"
                onClick={handleGenerate}
                onMouseEnter={handleGenerateMouseEnter}
                disabled={isGenerating}
                style={{
                  transform: `translate(${buttonPosition.x}px, ${buttonPosition.y}px) scale(${encouragementCount > 0 && !isGenerating ? Math.max(0.7, 1 - encouragementCount * 0.05) : 1})`,
                  transition: encouragementCount >= 7 ? 'transform 0.8s ease-out' : 'transform 0.3s ease-out'
                }}
              >
                {isGenerating ? (
                  <>
                    <span className="spinner"></span>
                    Generating your video pitch...
                  </>
                ) : (
                  'Generate Video Pitch 🎬'
                )}
              </button>
            </div>
          </div>
        ) : (
          <div className="result-section">
            <VideoPlayer videoUrl={videoUrl} />
            <button className="btn btn-primary" onClick={handleReset}>
              Create Another Video
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
